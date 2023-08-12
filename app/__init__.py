from flask import Flask
from flask_migrate import Migrate

from app.config_db import host, user, password, db_name
from app.models import db, main_models, Students, Groups, Courses, StudentCourse
# from app.views import groups_bp, students_bp, courses_bp, student_course_bp


def create_app(config_name):
    app = Flask(__name__)

    if config_name == 'production':
        app.config.from_object('app.config.production')
    elif config_name == 'testing':
        app.config.from_object('app.config.testing')
    else:
        app.config.from_object('app.config.development')

    db.init_app(app)
    migrate = Migrate(app, db)

    with app.app_context():
        main_models()

    # app.register_blueprint(groups_bp)
    # app.register_blueprint(students_bp)
    # app.register_blueprint(courses_bp)
    # app.register_blueprint(student_course_bp)

    return app
