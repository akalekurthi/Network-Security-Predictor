import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('instance/network_security.db')
cursor = conn.cursor()

# Write SQL query to find all users
query = """
SELECT id, username, email, created_at 
FROM user
ORDER BY id;
"""

print("Executing SQL query to find all users:")
print(query)
print("\nResults:")

# Execute the query and fetch results
try:
    cursor.execute(query)
    users = cursor.fetchall()
    
    # Display results in a formatted way
    if users:
        print(f"{'ID':<5} {'Username':<30} {'Email':<40} {'Created At':<20}")
        print("-" * 95)
        for user in users:
            print(f"{user[0]:<5} {user[1]:<30} {user[2]:<40} {user[3]:<20}")
        print(f"\nTotal users found: {len(users)}")
    else:
        print("No users found in the database.")
        
except sqlite3.Error as e:
    print(f"SQLite error: {e}")
    
# Close the connection
conn.close() 