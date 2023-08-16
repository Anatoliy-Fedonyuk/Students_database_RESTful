from faker import Faker

from models import db, Groups, Students, Courses, StudentCourse

faker = Faker()


def generate_groups():
    for _ in range(10):
        name = faker.bothify(text='??-##').upper()
        groups = Groups(name=name)
        db.session.add(groups)
    db.session.commit()
    print("[INFO] --Table 'groups' generated successfully--")


def generate_students():
    for _ in range(200):
        first_name = faker.unique.first_name()
        last_name = faker.unique.last_name()
        age = faker.random.randint(15, 60)
        group_id = faker.random.randint(1, 10)  # Выбираем случайную группу
        students = Students(first_name=first_name, last_name=last_name, age=age, group_id=group_id)
        db.session.add(students)
    db.session.commit()
    print("[INFO] --Table 'students' generated successfully--")


def generate_courses():
    course_names = ["Math", "Biology", "Chemistry", "Physics", "History",
                    "Literature", "Programming", "Art", "Music", "Economics"]

    descriptions = ["Study of exact fundamental natural science",
                    "Study of living organisms and their interactions",
                    "Study of matter and its properties",
                    "Study of matter, energy, and the forces of nature",
                    "Study of past events and human societies",
                    "Study of written and oral works of imagination",
                    "Study of algorithms, data structures, and problem-solving",
                    "Study of visual arts and creative expression",
                    "Study of sound, rhythm, and musical composition",
                    "Study of production, distribution, and consumption"]

    for course, description in zip(course_names, descriptions):
        courses = Courses(course=course, description=description)
        db.session.add(courses)
    db.session.commit()
    print("[INFO] --Table 'courses' generated successfully--")


def generate_student_course():
    students = Students.query.all()
    courses = Courses.query.all()

    for student in students:
        num_courses = faker.random.randint(1, 3)  # Случайное количество курсов от 1 до 3
        random_courses = faker.random.sample(courses, num_courses)
        for course in random_courses:
            student_course = StudentCourse(id_student=student.id, id_course=course.id_course)
            db.session.add(student_course)
    db.session.commit()
    print("[INFO] --Table 'student_course' generated successfully--")

# if __name__ == "__main__":
#     with app.app_context():
#         generate_groups()
#         generate_students()
#         generate_courses()
#         generate_student_course()
