import mysql.connector

# Database configuration
db_config = {
    "host": "mysql-2d50f4f1-xudoyberdiyevrahmatilla-b900.i.aivencloud.com",
    "port": 10187,
    "user": "avnadmin",
    "password": "AVNS_8pPnOCVBSgx4GU5dG3K",
    "database": "defaultdb",
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