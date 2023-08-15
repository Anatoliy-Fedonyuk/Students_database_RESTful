from flask import Flask
from importlib import import_module


def create_app(config_name):
    app = Flask(__name__)

    config_module = import_module(f'config.{config_name}')
    app.config.from_object(config_module)

    # app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:postgres@127.0.0.1/postgres'
    # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # app.register_blueprint(groups_bp)
    # app.register_blueprint(students_bp)
    # app.register_blueprint(courses_bp)
    # app.register_blueprint(student_course_bp)

    return app


if __name__ == "__main__":
    create_app('development')
