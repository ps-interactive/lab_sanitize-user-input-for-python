import sqlite3


def vulnerable_login(conn, username, password):
    cursor = conn.cursor()

    query = f"""
        SELECT *
        FROM users
        WHERE username = '{username}' AND password = '{password}'
    """

    print("Executing:")
    print(query)

    cursor.execute(query)

    return cursor.fetchone() is not None


# --- Main Execution ---

# 1. Connect directly to the existing database on disk
conn = sqlite3.connect("database.db")

# 2. Call the vulnerable login function
is_logged_in = vulnerable_login(conn, "admin", "SuperSecret123")
print(f"Login Successful? {is_logged_in}")

# 3. Always close the database connection when finished
conn.close()