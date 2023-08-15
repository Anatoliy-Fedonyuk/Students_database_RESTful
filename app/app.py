from sqlalchemy import inspect, func

from app.config_db import main_config
from app.generator import generate_groups, generate_students, generate_courses, generate_student_course
from app.init import create_app
from app.models import db, main_models
# from flask_migrate import Migrate


app = create_app('development')
db.init_app(app)
# migrate = Migrate(app, db)



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
        print("PostgreSQL version:", db.session.query(func.version()).scalar())


if __name__ == "__main__":
    check_tables()
    app.run(debug=True)
