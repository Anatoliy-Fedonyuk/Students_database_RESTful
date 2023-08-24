from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Groups(db.Model):
    group_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return f"Group :{self.group_id}, {self.name}"


class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False, unique=True)
    last_name = db.Column(db.String(50), nullable=False, unique=True)
    age = db.Column(db.Integer, nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'), nullable=False)

    def __repr__(self):
        return f"Student :{self.id}, {self.first_name}, {self.last_name}, {self.age}, {self.group_id}"


class Courses(db.Model):
    id_course = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f"Course :{self.id_course}, {self.course}, {self.description}"


class StudentCourse(db.Model):
    id_student = db.Column(db.Integer, db.ForeignKey('students.id'), primary_key=True, nullable=False)
    id_course = db.Column(db.Integer, db.ForeignKey('courses.id_course'), primary_key=True, nullable=False)
    __table_args__ = (db.UniqueConstraint('id_student', 'id_course', name='_student_course_uc'),)

    def __repr__(self):
        return f"Student&Course : {self.id_student}, {self.id_course}"


def create_tables():
    with db.session.begin():
        print("[INFO] --PostgreSQL connection opened--")
        db.create_all()
    print("[INFO] --Tables created successfully--")


def main_models():
    try:
        create_tables()
    except Exception as ex:
        print("[ERROR] Error while working with PostgreSQL :", ex)
    finally:
        db.session.close()
