from flask import Flask
from flask_migrate import Migrate
# from .models import db, main_models
# from app.views import groups_bp, students_bp, courses_bp, student_course_bp
# from config_db import host, user, password, db_name


def create_app(config_name):
    app = Flask(__name__)

    # app.config["SQLALCHEMY_DATABASE_URI"] = f'postgresql://{user}:{password}@{host}/{db_name}'
    # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if config_name == 'production':
        app.config.from_object('app.config.production')
    elif config_name == 'testing':
        app.config.from_object('app.config.testing')
    else:
        app.config.from_object('app.config.development')

    from .models import db
    db.init_app(app)
    migrate = Migrate(app, db)

    with app.app_context():
        from .models import main_models
        main_models()

    # app.register_blueprint(groups_bp)
    # app.register_blueprint(students_bp)
    # app.register_blueprint(courses_bp)
    # app.register_blueprint(student_course_bp)

    return app


if __name__ == "__main__":
    create_app('development')
