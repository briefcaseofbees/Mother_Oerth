import sqlite3
from sqlite3 import Error

_DB_FILE = "db.sqlite3"


def create_connection(db_file=_DB_FILE):
    """ create a database connection to the SQLite database"""

    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to SQLite database: {db_file}")
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None


def insert_user(conn, name, age):
    """Insert a new user into the users table."""
    try:
        sql_insert = "INSERT INTO users (name, age) VALUES (?, ?)"
        conn.execute(sql_insert, (name, age))
        conn.commit()
        print(f"Inserted user: {name}, Age: {age}")
    except Error as e:
        print(f"Error inserting user: {e}")


def fetch_users(conn):
    """Fetch all users from the users table."""
    try:
        cursor = conn.execute("SELECT id, name, age FROM users")
        rows = cursor.fetchall()
        print("\nUsers in database:")
        for row in rows:
            print(row)
    except Error as e:
        print(f"Error fetching users: {e}")