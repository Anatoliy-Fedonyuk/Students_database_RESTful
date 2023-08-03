from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Group(db.Model):
    group_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False, unique=True)
    last_name = db.Column(db.String(50), nullable=False, unique=True)
    age = db.Column(db.Integer, nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.group_id'), nullable=False)
    group = db.relationship('Group', backref='students')
    courses = db.relationship('Course', secondary='student_course')


class Course(db.Model):
    id_course = db.Column(db.Integer, primary_key=True)
    course = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(150), nullable=False)
    students = db.relationship('Student', secondary='student_course')


class StudentCourse(db.Model):
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id_course'), primary_key=True)


def create_tables():
    with db.session.begin():
        db.create_all()
    print("[INFO] Tables created successfully")


def main(user):
    try:
        with db.session.begin():
            create_tables()
            print("[INFO] PostgreSQL connection opened")

            # Здесь можно вызвать функции из generator.py для заполнения таблиц данными

    except Exception as ex:
        print("[ERROR] Error while working with PostgreSQL:", ex)

    finally:
        print("[INFO] PostgreSQL connection closed")
