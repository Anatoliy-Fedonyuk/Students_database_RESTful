from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Groups(db.Model):
    group_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)


class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False, unique=True)
    last_name = db.Column(db.String(50), nullable=False, unique=True)
    age = db.Column(db.Integer, nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'))


class Courses(db.Model):
    id_course = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(150), nullable=False)


class StudentCourse(db.Model):
    id_sc = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_student = db.Column(db.Integer, db.ForeignKey('students.id'))
    id_course = db.Column(db.Integer, db.ForeignKey('courses.id_course'))


def create_tables():
    with db.session.begin():
        print("[INFO] PostgreSQL connection opened")
        db.create_all()
    print("[INFO] Tables created successfully")


def main_models():
    try:
        create_tables()
        # Here we will further call the functions from generator.py to fill the tables with data

    except Exception as ex:
        print("[ERROR] Error while working with PostgreSQL:", ex)

    finally:
        db.session.close()
        print("[INFO] PostgreSQL connection closed")
