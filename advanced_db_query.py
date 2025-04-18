import sqlite3
import os
from datetime import datetime

def format_db_size(size_bytes):
    """Format bytes to a human-readable size"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024 or unit == 'GB':
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024

def advanced_db_query():
    # Database info
    db_path = 'instance/network_security.db'
    if not os.path.exists(db_path):
        print(f"Error: Database file not found at {db_path}")
        return
    
    db_size = os.path.getsize(db_path)
    print(f"Database: {db_path}")
    print(f"Size: {format_db_size(db_size)}")
    print(f"Last modified: {datetime.fromtimestamp(os.path.getmtime(db_path))}")
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("\n===== DETAILED DATABASE ANALYSIS =====")
    
    # 1. Get all tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = [row['name'] for row in cursor.fetchall()]
    
    print(f"\n1. Tables in database ({len(tables)}): {', '.join(tables)}")
    
    # 2. Analyze each table
    for table in tables:
        print(f"\n2. Table Analysis: {table}")
        
        # Get row count
        cursor.execute(f"SELECT COUNT(*) as count FROM {table};")
        row_count = cursor.fetchone()['count']
        print(f"   - Row count: {row_count}")
        
        # Get column info
        cursor.execute(f"PRAGMA table_info({table});")
        columns = cursor.fetchall()
        
        print(f"   - Columns ({len(columns)}):")
        for col in columns:
            print(f"     • {col['name']} ({col['type']}){' PRIMARY KEY' if col['pk'] else ''}{' NOT NULL' if col['notnull'] else ''}")
    
    # 3. User information with security analysis (if user table exists)
    if 'user' in tables:
        print("\n3. User Security Analysis:")
        
        # a. Password hash distribution
        cursor.execute("""
        SELECT 
            length(password_hash) as hash_length,
            COUNT(*) as count
        FROM user
        GROUP BY length(password_hash)
        ORDER BY hash_length;
        """)
        hash_dist = cursor.fetchall()
        
        if hash_dist:
            print("   - Password hash length distribution:")
            for row in hash_dist:
                print(f"     • Length {row['hash_length']} characters: {row['count']} users")
        
        # b. User creation timeline
        cursor.execute("""
        SELECT 
            strftime('%Y-%m-%d', created_at) as date,
            COUNT(*) as count
        FROM user
        GROUP BY date
        ORDER BY date;
        """)
        timeline = cursor.fetchall()
        
        if timeline:
            print("   - User registration timeline:")
            for row in timeline:
                print(f"     • {row['date']}: {row['count']} users registered")
        
        # c. Sample user data (only showing non-sensitive information)
        cursor.execute("""
        SELECT 
            id, 
            username, 
            substr(email, 1, 3) || '...' || substr(email, instr(email, '@')) as masked_email,
            created_at
        FROM user
        ORDER BY id
        LIMIT 5;
        """)
        users = cursor.fetchall()
        
        if users:
            print("   - Sample users (with masked emails):")
            for user in users:
                print(f"     • ID {user['id']}: {user['username']} ({user['masked_email']}) - Created: {user['created_at']}")
    
    # 4. Database integrity check
    print("\n4. Database Integrity Check:")
    cursor.execute("PRAGMA integrity_check;")
    integrity = cursor.fetchone()
    print(f"   - Result: {integrity[0]}")
    
    conn.close()
    print("\n===== END OF DATABASE ANALYSIS =====")

if __name__ == "__main__":
    advanced_db_query() 