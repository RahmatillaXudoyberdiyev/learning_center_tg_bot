import subprocess
import mysql.connector.pooling
from aiogram.types import Message, BufferedInputFile
from io import BytesIO
from datetime import datetime
from config import MySQL_password, MySQL_database, MySQL_host, MySQL_port, MySQL_user

try:
    from openpyxl import Workbook
except ImportError:
    subprocess.run(["pip", "install", "openpyxl"])
    from openpyxl import Workbook

# MySQL Connection Pool
DB_CONFIG = {
    "host": MySQL_host,
    "port": MySQL_port,
    "user": MySQL_user,
    "password": MySQL_password,
    "database": MySQL_database,
}
connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    **DB_CONFIG
)

def fetch_data(query, params=None):
    connection = connection_pool.get_connection()
    cursor = connection.cursor()
    cursor.execute(query, params or ())
    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return columns, data

def create_excel_file(columns, data):
    wb = Workbook()
    ws = wb.active
    ws.append(columns)
    for row in data:
        ws.append(row)
    excel_file = BytesIO()
    wb.save(excel_file)
    excel_file.seek(0)
    return excel_file

async def all_reports(message: Message):
    query = """
        SELECT users.id, users.full_name, users.phone, users.datetime, users.username, users.t_id,
               courses.name AS course_name, branches.name AS branch_name, regions.name AS region_name
        FROM users
        JOIN courses ON users.course_id = courses.id
        JOIN branches ON users.branch_id = branches.id
        JOIN regions ON branches.region_id = regions.id
    """
    columns, data = fetch_data(query)
    if not data:
        await message.answer("No data found in the users table.")
        return
    excel_file = create_excel_file(columns, data)
    await message.answer_document(
        BufferedInputFile(excel_file.read(), filename="all_users.xlsx")
    )

async def today_reports(message: Message):
    today = datetime.today().strftime('%Y-%m-%d')
    query = """
        SELECT users.id, users.full_name, users.phone, users.datetime, users.username, users.t_id,
               courses.name AS course_name, branches.name AS branch_name, regions.name AS region_name
        FROM users
        JOIN courses ON users.course_id = courses.id
        JOIN branches ON users.branch_id = branches.id
        JOIN regions ON branches.region_id = regions.id
        WHERE DATE(users.datetime) = %s
    """
    columns, data = fetch_data(query, (today,))
    if not data:
        await message.answer("No data found for today.")
        return
    excel_file = create_excel_file(columns, data)
    await message.answer_document(
        BufferedInputFile(excel_file.read(), filename="users_today.xlsx")
    )