import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    # Fetch a connection from the pool
    try:
        # Create a single connection
        connection = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            user=os.getenv('MYSQL_USER'),
            password="mtgnLiiYtQbQKXgphtSn",
            database=os.getenv('MYSQL_DB'),
            port=os.getenv('MYSQL_PORT'),
        )
        if connection.is_connected():
            print("Connected to the database successfully")
    except mysql.connector.Error as e:
        print(f"Error connecting to the database: {e}")
        connection = None
