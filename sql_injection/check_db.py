import sqlite3


conn = sqlite3.connect("database.db")

# Create a cursor to query the database
cursor = conn.cursor()

# Query all rows from the users table
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()

# Print the results
for row in rows:
    print(row)

# Close the database connection
conn.close()