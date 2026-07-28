## Key Takeaways

| Vulnerable Practice     | Secure Practice                                           |
|-------------------------|-----------------------------------------------------------|
| f-strings in SQL        | Parameterized queries (`?`, `%s`, named parameters)       |
| `%` string formatting   | ORM frameworks (SQLAlchemy, Django ORM)                   |
| String concatenation    | Prepared statements                                       |
| User input becomes SQL  | User input remains data                                   |


## Security Lessons
- Never construct SQL statements with f-strings, % formatting, or string concatenation.

- Use parameterized queries provided by the database driver (such as sqlite3 or psycopg2).

- Modern ORM frameworks like SQLAlchemy and Django ORM generate parameterized SQL by default, providing an additional layer of protection against SQL injection.