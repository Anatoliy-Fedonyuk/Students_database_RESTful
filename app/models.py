import psycopg2
from config import host, user, password, db_name

try:
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {user};")
        print(f"[INFO] User '{user}' rights set for the database '{db_name}'")

        cursor.execute("SELECT version();")
        print(f'Server version: {cursor.fetchone()}')

        cursor.execute("SELECT * FROM users;")
        [print(res) for res in cursor]


except Exception as _ex:
    if connection: connection.rollback()
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:
    if connection: connection.close()
    print("[INFO] PostgreSQL connection closed")