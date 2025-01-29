import os
import mysql.connector
from mysql.connector import pooling, Error
from dotenv import load_dotenv

load_dotenv()

# Database Configuration
db_config = {
    "host": os.getenv('MYSQL_HOST'),
    "user": os.getenv('MYSQL_USER'),
    "password": os.getenv('MYSQL_PASSWORD'),  # Store password in .env file
    "database": os.getenv('MYSQL_DB'),
    "port": int(os.getenv('MYSQL_PORT', 3306)),  # Convert port to integer
    "autocommit": True  # Ensures auto-commit mode is enabled
}

# Create a Connection Pool (Max 3 connections to avoid exceeding the limit)
try:
    connection_pool = pooling.MySQLConnectionPool(
        pool_name="mypool",
        pool_size=5,  # Keep this under the limit
        pool_reset_session=True,  # Reset session variables on reuse
        **db_config
    )
    print("✅ MySQL Connection Pool Created Successfully (Max 3 Connections)")
except Error as e:
    print(f"❌ Error creating connection pool: {e}")
    connection_pool = None  # Avoid using an invalid pool

def get_connection():
    """Get a connection from the pool, ensuring it's alive"""
    global connection_pool
    if not connection_pool:
        print("⚠️ Connection pool not available. Returning None.")
        return None

    try:
        connection = connection_pool.get_connection()
        connection.ping(reconnect=True, attempts=3, delay=2)  # Ensure connection is alive
        return connection
    except Error as e:
        print(f"❌ Error getting a database connection: {e}")
        return None
