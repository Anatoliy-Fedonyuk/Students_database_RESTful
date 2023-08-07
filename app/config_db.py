import psycopg2
from tabulate import tabulate

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


def sql_get():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute("""SELECT g.name, count(s.id)
                            FROM groups g 
                            LEFT JOIN students s ON g.group_id = s.group_id 
                            GROUP BY g.name
                            HAVING count(s.id) = (
                                SELECT count(s.id)
                                FROM students s 
                                GROUP BY s.group_id
                                ORDER BY count(s.id) ASC
                                LIMIT 1);""")

            headers = ["Group", "Count Students"]
            print(tabulate(cursor.fetchall(), headers, tablefmt="psql"))

            cursor.execute("""select c.course, s.first_name, s.last_name 
                            from student_course sc
                            left join students s on s.id=sc.id_student
                            left join courses c on c.id_course=sc.id_course
                            where c.course = 'Art';""")

            headers = ["№", "Course", "First Name", "Last Name"]
            print(tabulate(cursor.fetchall(), headers, showindex=True, tablefmt="psql"))

            # cursor.execute("""INSERT INTO students (first_name, last_name, age)
            #                 VALUES ('Robot', 'Robot', 33);""")
            cursor.execute("select * from students where id>=190 order by id desc;")
            print(cursor.fetchall())

            # cursor.execute("""DELETE FROM students WHERE id = 201;""")







    except Exception as ex:
        print("[ERROR] Error while working with PostgreSQL:", ex)

    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")


if __name__ == "__main__":
    # main()
    sql_get()
