import os
import mysql.connector
from mysql.connector import pooling

from dotenv import load_dotenv

load_dotenv()


class Database:
    def __init__(self):
        # Create a connection pool
        self.pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name="my_connection_pool",
            pool_size=10, 
            pool_reset_session=True,
            host=os.getenv('MYSQL_HOST'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            database=os.getenv('MYSQL_DB')
        )
        print("Connection pool created successfully")

    def get_connection(self):
        # Fetch a connection from the pool
        try:
            connection = self.pool.get_connection()
            if connection.is_connected():
                print("Connection obtained from pool")
                return connection
        except mysql.connector.Error as e:
            print(f"Error obtaining connection from pool: {e}")
            return None
