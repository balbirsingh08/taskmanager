# debug_db.py
import sqlite3

def check_database():
    try:
        conn = sqlite3.connect('taskmanager.db')
        cursor = conn.cursor()
        
        # Check if users table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("Tables in database:", tables)
        
        # Check users table structure
        cursor.execute("PRAGMA table_info(users);")
        users_columns = cursor.fetchall()
        print("Users table columns:", users_columns)
        
        # Check all data in users table
        cursor.execute("SELECT * FROM users;")
        users = cursor.fetchall()
        print("All users data:", users)
        
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_database()