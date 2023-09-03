"""The MAIN module of our FLASK RESTFUL API application - <SQL>"""
from flask import Flask, redirect, url_for
from flask_restful import Api
from importlib import import_module
from flasgger import Swagger
from flask_limiter import Limiter
import logging
# from flask_migrate import Migrate

from src.models import db
from src.views.students import StudentsListResource, StudentResource, CreateStudentResource
from src.views.groups import AllGroupsResource, GroupsOnRequestResource
from src.views.courses import CoursesAllResource, CourseUpdateResource
from src.views.student_course import StudentsInCourseResource, StudentCourseResource, OneStudentCoursesResource


def register_resources(api: Api) -> None:
    """Register resources with the given Api."""
    api.add_resource(StudentsListResource, '/students/')
    api.add_resource(StudentResource, '/students/<int:id>')
    api.add_resource(CreateStudentResource, '/students/')
    #
    api.add_resource(AllGroupsResource, '/groups/students')
    api.add_resource(GroupsOnRequestResource, '/groups/<int:num>/students')
    #
    api.add_resource(CoursesAllResource, '/courses/')
    api.add_resource(CourseUpdateResource, '/courses/<int:id>')
    #
    api.add_resource(StudentsInCourseResource, '/courses/<string:course>/students/')
    api.add_resource(OneStudentCoursesResource, '/students/<int:id>/courses/')
    api.add_resource(StudentCourseResource, '/students/<int:id_student>/courses/<int:id_course>')


def create_app(config_name: str) -> Flask:
    """Create a Flask src using the provided configuration name."""
    app = Flask(__name__)

    config_module = import_module(f'config.{config_name}')
    app.config.from_object(config_module)

    Limiter(app)

    db.init_app(app)
    # migrate = Migrate(src, db)
    api = Api(app, prefix='/api/v1')
    Swagger(app, template_file='swagger/swagger.yml')
    register_resources(api)

    configure_logging(app)

    @app.route('/')
    def index():
        """Redirect to API documentation for developers."""
        return redirect(url_for('flasgger.apidocs', _external=True))

    return app


def configure_logging(app):
    """Logging level setting and log file."""
    log_level = app.config.get('LOG_LEVEL', 'INFO')
    log_file = app.config.get('LOG_FILE', None)

    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)


if __name__ == "__main__":
    app = create_app('production')
    app.run()
