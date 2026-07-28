import sqlite3

def setup_database():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE users (
            username TEXT,
            password TEXT
        )
    """)

    cursor.execute(
        "INSERT INTO users VALUES (?, ?)",
        ("admin", "SuperSecret123")
    )

    cursor.execute(
        "INSERT INTO users VALUES (?, ?)",
        ("alice", "Password1")
    )

    conn.commit()
    return conn

conn = setup_database()