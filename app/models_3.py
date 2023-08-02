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

    # with connection.cursor() as cursor:
    #     cursor.execute(
    #         "SELECT version();")
    #     print(f"Server version: {cursor.fetchone()}")

    # with connection.cursor() as cursor:
    #     cursor.execute(
    #         """CREATE TABLE users(
    #             id serial PRIMARY KEY,
    #             first_name varchar(50) NOT NULL,
    #             nick_name varchar(50) NOT NULL);""")
    #     print("[INFO] Table created successfully")

    new_users = [('Oleg', 'barracuda'),
                 ('Anatol', 'tiger'),
                 ('Serge', 'chupacabra'),
                 ('Vovan', 'pastor')]

    # with connection.cursor() as cursor:
    #     cursor.executemany("INSERT INTO users VALUES (default, %s, %s);", new_users)
    #     print("[INFO] Data was successfully inserted")

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users;")
        [print(res) for res in cursor]
        cursor.execute("SELECT nick_name FROM users WHERE first_name = 'Oleg';")
        print(cursor.fetchone())
        cursor.execute("SELECT nick_name FROM users WHERE first_name = 'Vovan' AND id >= 8;")
        print(cursor.fetchall())
        cursor.execute("SELECT count(id) FROM users;")
        print(cursor.fetchone())
        cursor.execute("SELECT * FROM users WHERE id>=5 AND id<=12 ORDER BY nick_name DESC;")
        [print(res) for res in cursor]
        cursor.execute("SELECT version();")
        print(f'Server version: {cursor.fetchone()}')


    # delete a table
    # with connection.cursor() as cursor:
    #     cursor.execute("DROP TABLE users;")
    #     print("[INFO] Table was deleted")

except Exception as _ex:
    if connection: connection.rollback()
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:
    if connection: connection.close()
    print("[INFO] PostgreSQL connection closed")
