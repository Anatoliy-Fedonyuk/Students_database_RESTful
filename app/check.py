"""This module is for checking whether it is a new empty database, if so,
 then we create all models for the database and generate data for their correct filling."""

from sqlalchemy import inspect, func

from init import app
from models import db, main_models
from generator import generate_groups, generate_students, generate_courses, generate_student_course


def check_tables() -> str:
    """In this function, all tasks of the module are performed"""
    with app.app_context():
        ins = inspect(db.engine)
        tables_exist = all(ins.has_table(tab) for tab in ['groups', 'students', 'courses', 'student_course'])
        if not tables_exist:
            print(main_models())
            print(generate_groups())
            print(generate_students())
            print(generate_courses())
            print(generate_student_course())
            return "[INFO] --PostgreSQL connection closed--"
        else:
            print("PostgreSQL version:", db.session.query(func.version()).scalar())
            return "[INFO] --The ORM-models PostgreSQL already exist!--"


if __name__ == "__main__":
    print(check_tables())
