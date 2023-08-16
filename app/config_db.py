# from random import randint
# import psycopg2
# from tabulate import tabulate

host = "127.0.0.1"
user = "postgres"
password = "postgres"
db_name = "postgres"
port = "5432"


def main_config():
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
            """---Find all groups with less or equals student count---"""
            cursor.execute("""SELECT g.name, count(s.id)
                            FROM groups g 
                            LEFT JOIN students s ON g.group_id = s.group_id 
                            GROUP BY g.name
                            HAVING  count(s.id) = (
                                SELECT count(s.id)
                                FROM students s 
                                GROUP BY s.group_id
                                ORDER BY count(s.id) ASC
                                LIMIT 1);""")
            headers = ["Group", "Count Students"]
            print(tabulate(cursor.fetchall(), headers, tablefmt="psql"))

            """---Find all students related to the course with a given name---"""
            cursor.execute("""select c.course, s.first_name, s.last_name
                            from student_course sc
                            left join students s on s.id=sc.id_student
                            left join courses c on c.id_course=sc.id_course
                            where c.course = 'History';""")
            headers = ["№", "Course", "First Name", "Last Name"]
            print(tabulate(cursor.fetchall(), headers, showindex=True, tablefmt="mixed_outline"))

            """---Add new student !---"""
            cursor.execute(f"""INSERT INTO students (first_name, last_name, age, group_id)
                            VALUES ('Robot', 'Robot', 33, {randint(1,10)});""")
            cursor.execute("select * from students where id>=190 order by id;")
            headers = ["№", "First Name", "Last Name", "Age", "Group"]
            print(tabulate(cursor.fetchall(), headers, tablefmt="mixed_outline"))

            """---Delete student by STUDENT_ID !---"""
            num_student = 200
            cursor.execute(f"SELECT * FROM students WHERE id = {num_student};")
            if cursor.fetchone():
                cursor.execute(f"DELETE FROM student_course WHERE id_student = {num_student};")
                cursor.execute(f"DELETE FROM students WHERE id = {num_student};")
            else:
                print("[ERROR] Error this student does not exist!")
            cursor.execute("select * from students where id>=190 order by id;")
            headers = ["№", "First Name", "Last Name", "Age", "Group"]
            print(tabulate(cursor.fetchall(), headers, tablefmt="mixed_outline"))

            """---Add a student to the course (from a list)---"""
            num_student, name_course = 204, 'Art'
            cursor.execute(f"""INSERT INTO student_course (id_student, id_course)
            VALUES ({num_student}, (select c.id_course from courses c where c.course='{name_course}'));""")
            cursor.execute(f"""select s.first_name, s.last_name, c.course
                                        from student_course sc
                                        left join students s on s.id=sc.id_student
                                        left join courses c on c.id_course=sc.id_course
                                        where s.id='{num_student}';""")
            headers = ["First Name", "Last Name", "Course"]
            print(tabulate(cursor.fetchall(), headers, tablefmt="mixed_outline"))

            """---Remove the student from one of his or her courses---"""
            student_id, course_id = 204, 8
            cursor.execute(f"DELETE FROM student_course WHERE id_student = {student_id} AND id_course = {course_id};")
            cursor.execute(f"""select s.first_name, s.last_name, c.course
                                                    from student_course sc
                                                    left join students s on s.id=sc.id_student
                                                    left join courses c on c.id_course=sc.id_course
                                                    where s.id='{num_student}';""")
            headers = ["First Name", "Last Name", "Course"]
            print(tabulate(cursor.fetchall(), headers, tablefmt="mixed_outline"))


    except Exception as ex:
        print("[ERROR] Error while working with PostgreSQL:", ex)

    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")


if __name__ == "__main__":
    main_config()
    # sql_get()