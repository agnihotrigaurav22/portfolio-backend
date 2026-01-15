import pymysql
import os
from config import Config

# Parse the URI or just use the config values directly since we know the logic
host = os.environ.get('DB_HOST') or 'localhost'
user = os.environ.get('DB_USER') or 'root'
password = os.environ.get('DB_PASS') or ''
db_name = os.environ.get('DB_NAME') or 'portfolio_db'

print(f"Connecting to MySQL at {host} as {user}...")

try:
    conn = pymysql.connect(host=host, user=user, password=password)
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    print(f"Database '{db_name}' check/creation successful.")
    conn.close()
except Exception as e:
    print(f"Error creating database: {e}")
    print("Please ensure MySQL is running and credentials are correct.")
    exit(1)
