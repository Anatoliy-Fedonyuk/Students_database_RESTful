from init import create_app
from sqlalchemy import inspect, func
from flask_migrate import Migrate

from models import db, main_models, Students
# from config_db import main_config
from generator import generate_groups, generate_students, generate_courses, generate_student_course

app = create_app('development')
db.init_app(app)
migrate = Migrate(app, db)


def check_tables():
    with app.app_context():
        ins = inspect(db.engine)
        tables_exist = all(ins.has_table(tab) for tab in ['groups', 'students', 'courses', 'student_course'])
        if not tables_exist:
            # main_config()
            main_models()
            generate_groups()
            generate_students()
            generate_courses()
            generate_student_course()
            print("[INFO] PostgreSQL connection closed")
        print("PostgreSQL version:", db.session.query(func.version()).scalar())



if __name__ == "__main__":
    check_tables()
    app.run(debug=True)
