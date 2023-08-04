from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Groups(db.Model):
    group_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)


class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False, unique=True)
    last_name = db.Column(db.String(50), nullable=False, unique=True)
    age = db.Column(db.Integer, nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'), nullable=False)
    group = db.relationship('Groups', backref='students')
    courses = db.relationship('Courses', secondary='students_courses')


class Courses(db.Model):
    id_course = db.Column(db.Integer, primary_key=True)
    course = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(150), nullable=False)
    students = db.relationship('Students', secondary='students_courses')


class StudentCourse(db.Model):
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id_course'), primary_key=True)


def create_tables():
    with db.session.begin():
        db.create_all()
    print("[INFO] Tables created successfully")


def main():
    try:
        with db.session.begin():
            create_tables()
            print("[INFO] PostgreSQL connection opened")
            # Here we will further call the functions from generator.py to fill the tables with data

    except Exception as ex:
        print("[ERROR] Error while working with PostgreSQL:", ex)

    finally:
        print("[INFO] PostgreSQL connection closed")
