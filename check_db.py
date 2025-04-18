import sqlite3
import os

def check_database():
    try:
        # Print the current directory
        print(f"Current directory: {os.getcwd()}")
        
        # Check if database file exists
        db_path = 'instance/network_security.db'
        if os.path.exists(db_path):
            print(f"Database file exists at: {db_path}")
            print(f"Database size: {os.path.getsize(db_path)} bytes")
        else:
            print(f"Database file not found at: {db_path}")
            # Try to search for the file
            for root, dirs, files in os.walk('.'):
                for file in files:
                    if file.endswith('.db'):
                        print(f"Found database file: {os.path.join(root, file)}")
        
        # Try to connect to the database
        conn = sqlite3.connect(db_path)
        print("Successfully connected to the database")
        
        # Get list of tables
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"Tables in the database: {tables}")
        
        # Check each table structure
        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            print(f"\nTable: {table_name}")
            print("Columns:")
            for col in columns:
                print(f"  {col[1]} ({col[2]})")
        
        # Check for any users in the User table if it exists
        if ('user',) in tables or ('User',) in tables:
            table_name = 'user' if ('user',) in tables else 'User'
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            user_count = cursor.fetchone()[0]
            print(f"\nNumber of users in the database: {user_count}")
            
            if user_count > 0:
                cursor.execute(f"SELECT id, username, email FROM {table_name} LIMIT 5;")
                users = cursor.fetchall()
                print("Sample users (ID, Username, Email):")
                for user in users:
                    print(f"  {user}")
        
        conn.close()
        
    except Exception as e:
        print(f"Error checking database: {str(e)}")

if __name__ == "__main__":
    check_database() 