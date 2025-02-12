from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from admin_panel.keyboards.begin_keyboards import get_keyboard
from admin_panel.states.process_track_state import ProcessTrack
import mysql.connector.pooling
from config import MySQL_password, MySQL_database, MySQL_host, MySQL_port, MySQL_user
from aiogram.types import ReplyKeyboardRemove
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

async def send_news(message: Message, state: FSMContext):

    await message.answer("Iltimos foydalanuvchiga nima yubormoqchi bo'lsangiz shu yerga jo'nating:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(ProcessTrack.send_news)

async def process_send_news(message: Message, state: FSMContext):

    columns, users = fetch_data("SELECT t_id FROM users")
    if not users:
        await message.answer("No users found in the database.")
        await state.clear()  
        return

    user_ids = [user[0] for user in users]

    successful_sends = 0
    failed_sends = 0
    for user_id in user_ids:
        try:
            await message.bot.send_message(user_id, message.text)
            successful_sends += 1
        except Exception:
            failed_sends += 1
            continue

    await message.answer(
        f"{successful_sends} ta foydalanuvchilarga muvaffaqiyatli jo'natildi.\n"
        f"{failed_sends} ta foydalanuvchi botni o'chirib tashlabdi ."
    )

    await state.clear()
    await state.set_state(ProcessTrack.chosen_menu)

# Admin start command
async def admin_start_command(message: Message, state: FSMContext):
    await message.answer("Assalomu aleykum admin botga xush kelibsiz", reply_markup=get_keyboard())
    await state.clear()
    await state.set_state(ProcessTrack.chosen_menu)