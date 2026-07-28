# ORM Example (SQLAlchemy)
# ORM frameworks automatically parameterize queries.

from sqlalchemy import select

def login(session, username, password):
    stmt = (
        select(User)
        .where(User.username == username)
        .where(User.password == password)
    )

    return session.execute(stmt).scalar_one_or_none()

# The generated SQL uses bound parameters instead of concatenated strings, preventing SQL injection.

# Django ORM Example
user = User.objects.filter(
    username=username,
    password=password
).first()

if user:
    print("Login successful")
else:
    print("Login failed")

# Django ORM also uses parameterized queries internally, so user input is handled safely.