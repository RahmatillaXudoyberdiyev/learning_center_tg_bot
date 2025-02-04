import mysql.connector
from mysql.connector import Error

# Database configuration
db_config = {
    "host": "mysql-2d50f4f1-xudoyberdiyevrahmatilla-b900.i.aivencloud.com",
    "port": 10187,
    "user": "avnadmin",
    "password": "AVNS_8pPnOCVBSgx4GU5dG3K",
    "database": "defaultdb",
}

def check_database():
    try:
        # Connect to the database
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print("Successfully connected to the database!")

            # Create a cursor object
            cursor = connection.cursor()

            # Check if the required tables exist
            required_tables = ["regions", "branches", "courses"]
            cursor.execute("SHOW TABLES")
            existing_tables = [table[0] for table in cursor.fetchall()]

            missing_tables = [table for table in required_tables if table not in existing_tables]
            if missing_tables:
                print(f"Missing tables: {', '.join(missing_tables)}")
            else:
                print("All required tables exist.")

            # Check if the `course_branch_region` view exists
            cursor.execute("SHOW FULL TABLES WHERE TABLE_TYPE = 'VIEW'")
            existing_views = [view[0] for view in cursor.fetchall()]
            if "course_branch_region" not in existing_views:
                print("The `course_branch_region` view does not exist.")
            else:
                print("The `course_branch_region` view exists.")

            # Verify data in the tables
            for table in required_tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                row_count = cursor.fetchone()[0]
                print(f"Table `{table}` contains {row_count} rows.")

    except Error as e:
        print(f"Error: {e}")

    finally:
        # Close the connection
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Database connection closed.")

# Run the function
check_database()