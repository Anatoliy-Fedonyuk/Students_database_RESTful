# from flask import Flask
# from flask_migrate import Migrate
#
# from models import db, main_models, Students, Groups, Courses, StudentCourse
# from config_db import host, user, password, db_name, main_config
# from generator import generate_groups, generate_students, generate_courses, generate_student_course
#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}/{db_name}'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#
# db.init_app(app)
# migrate = Migrate(app, db)
from app import create_app
from sqlalchemy import inspect

app = create_app('development')


def check_tables():
    with app.app_context():
        ins = inspect(db.engine)
        tables_exist = all(ins.has_table(tab) for tab in ['groups', 'students', 'courses', 'student_course'])
        if not tables_exist:
            main_config()
            main_models()
            generate_groups()
            generate_students()
            generate_courses()
            generate_student_course()
            print("[INFO] PostgreSQL connection closed")
            print(db.session.query(Students).all())


# Далее тут пропишем все ендпоинты!


if __name__ == "__main__":
    check_tables()
    app.run(debug=True)
