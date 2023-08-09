import psycopg2
from config_db import host, user, password, db_name


def grant_user_privileges(conn, db, superuser):
    with conn.cursor() as cursor:
        cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {db} TO {superuser};")
        print(f"[INFO] User '{superuser}' rights set for the database '{db}'")


def create_tables(conn):
    with conn.cursor() as cursor:
        try:
            cursor.execute("""CREATE TABLE IF NOT EXISTS groups
                            (group_id serial PRIMARY KEY,
                            name varchar(50) NOT NULL UNIQUE);""")
            print("[INFO] Table 'groups' created successfully")

            cursor.execute("""CREATE TABLE IF NOT EXISTS students
                            (id serial PRIMARY KEY,
                            first_name varchar(50) NOT NULL UNIQUE,
                            last_name varchar(50) NOT NULL UNIQUE,
                            age INTEGER NOT NULL,
                            group_id INTEGER REFERENCES groups(group_id));""")
            print("[INFO] Table 'students' created successfully")

            cursor.execute("""CREATE TABLE IF NOT EXISTS courses
                            (id_course serial PRIMARY KEY,
                            course varchar(50) NOT NULL UNIQUE,
                            description varchar(150) NOT NULL);""")
            print("[INFO] Table 'courses' created successfully")

        except Exception as ex:
            print("[ERROR] Error while creating tables:", ex)


def main():
    connection = None

    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True

        grant_user_privileges(connection, db_name, user)
        print("[INFO] PostgreSQL connection opened")

        create_tables(connection)

    except Exception as ex:
        print("[ERROR] Error while working with PostgreSQL:", ex)

    finally:
        if connection is not None:
            connection.close()
            print("[INFO] PostgreSQL connection closed")


if __name__ == "__main__":
    main()