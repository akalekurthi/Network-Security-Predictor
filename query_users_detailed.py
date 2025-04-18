import sqlite3
import os

def run_sql_query():
    # Get information about the database
    db_path = 'instance/network_security.db'
    db_size = os.path.getsize(db_path) if os.path.exists(db_path) else 0
    print(f"Database file: {db_path}")
    print(f"Database size: {db_size} bytes")
    
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # This enables column access by name
    cursor = conn.cursor()
    
    # First query: Get user information with password hash length
    user_query = """
    SELECT 
        id, 
        username, 
        email, 
        created_at,
        length(password_hash) as password_hash_length
    FROM user
    ORDER BY id;
    """
    
    print("\n1. SQL Query for User Information:")
    print(user_query)
    
    cursor.execute(user_query)
    users = cursor.fetchall()
    
    if users:
        print("\nUser Results:")
        print(f"{'ID':<5} {'Username':<25} {'Email':<35} {'Created At':<25} {'Password Hash Length':<20}")
        print("-" * 110)
        for user in users:
            print(f"{user['id']:<5} {user['username']:<25} {user['email']:<35} {user['created_at']:<25} {user['password_hash_length']:<20}")
        print(f"\nTotal users: {len(users)}")
    else:
        print("\nNo users found.")
    
    # Second query: Get database schema information
    schema_query = """
    SELECT 
        m.name as table_name,
        p.name as column_name,
        p.type as column_type,
        p.'notnull' as not_null,
        p.pk as primary_key
    FROM 
        sqlite_master m
    JOIN 
        pragma_table_info(m.name) p
    WHERE 
        m.type = 'table' AND
        m.name NOT LIKE 'sqlite_%'
    ORDER BY 
        m.name, p.cid;
    """
    
    print("\n2. SQL Query for Database Schema:")
    print(schema_query)
    
    cursor.execute(schema_query)
    schema_info = cursor.fetchall()
    
    if schema_info:
        current_table = None
        print("\nDatabase Schema:")
        for row in schema_info:
            if current_table != row['table_name']:
                current_table = row['table_name']
                print(f"\nTable: {current_table}")
                print(f"{'Column Name':<20} {'Type':<15} {'Not Null':<10} {'Primary Key':<12}")
                print("-" * 60)
            
            print(f"{row['column_name']:<20} {row['column_type']:<15} {'Yes' if row['not_null'] else 'No':<10} {'Yes' if row['primary_key'] else 'No':<12}")
    
    # Close the connection
    conn.close()

if __name__ == "__main__":
    run_sql_query() 