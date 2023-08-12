from app import create_app, db, main_models, Students
from sqlalchemy import inspect

from app.config_db import main_config
from app.generator import generate_groups, generate_students, generate_courses, generate_student_course

app = create_app('config.development')


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
