import sqlite3

# Secure Version Using Parameterized Queries
# Instead of inserting values into the SQL string, use placeholders.
def secure_login(conn, username, password):
    cursor = conn.cursor()

    query = """
        SELECT *
        FROM users
        WHERE username = ?
        AND password = ?
    """

    print("Executing parameterized query")

    cursor.execute(query, (username, password))

    return cursor.fetchone() is not None

# --- 1. Establish the missing connection; connect db file on disk
conn = sqlite3.connect("database.db")

# --- 2. Testing with the same attack:
print(
    secure_login(
        conn,
        "admin' --",
        "does_not_matter"
    )
)
# Output: False
# The input is treated as plain text, not executable SQL.


# Why Parameterized Queries Work
# The SQL statement sent to SQLite is conceptually:
SELECT *
FROM users
WHERE username = ?
AND password = ?

# The database receives:
# Parameter 1:
# admin' --

# Parameter 2:
# does_not_matter

# => The values are never interpreted as SQL commands.

# --- 3. Close the connection ---
conn.close()
