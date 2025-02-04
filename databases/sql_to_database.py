import mysql.connector

from config import MySQL_password, MySQL_database, MySQL_host, MySQL_port, MySQL_user

db_config = {
    "host": MySQL_host,
    "port": MySQL_port,
    "user": MySQL_user,
    "password": MySQL_password,
    "database": MySQL_database,
}

# Connect to the database
db = mysql.connector.connect(**db_config)
cursor = db.cursor()

# Read and filter SQL file
with open("./data.sql", "r") as file:
    sql_commands = file.read().split(";")

# Define restricted keywords
restricted_keywords = [
    "CREATE DATABASE", 
    "USE ", 
    "GRANT ", 
    "SET SQL_MODE", 
    "CREATE VIEW", 
    "DEFINER"
]

# Execute SQL commands
for command in sql_commands:
    if command.strip() and not any(keyword in command for keyword in restricted_keywords):
        try:
            cursor.execute(command)
        except mysql.connector.Error as err:
            print(f"Skipping command: {command}\nError: {err}")

# Commit changes and close the connection
db.commit()
cursor.close()
db.close()

print("SQL file imported successfully (excluding restricted commands)!")