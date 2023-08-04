import psycopg2

host = "127.0.0.1"
user = "postgres"
password = "postgres"
db_name = "postgres"
port = "5432"


def main():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True

        with connection.cursor() as cursor:
            print("[INFO] PostgreSQL connection opened")

            cursor.execute("SELECT version();")
            print(f"Version DB: {cursor.fetchone()[0]}")

            cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {user};")
            print(f"[INFO] User '{user}' rights set for the database '{db_name}'")

    except Exception as ex:
        print("[ERROR] Error while working with PostgreSQL:", ex)

    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")


if __name__ == "__main__":
    main()
