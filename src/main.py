"""The MAIN module of our FLASK RESTFUL API application - <SQL>"""
from flask import Flask, redirect, url_for
from flask_restful import Api
from importlib import import_module
from flasgger import Swagger
from flask_limiter import Limiter
from loguru import logger
# from flask_migrate import Migrate

from src.models import db
from src.views.students import StudentsListResource, StudentResource, CreateStudentResource
from src.views.groups import AllGroupsResource, GroupsOnRequestResource
from src.views.courses import CoursesAllResource, CourseUpdateResource
from src.views.student_course import StudentsInCourseResource, StudentCourseResource, OneStudentCoursesResource


def register_resources(api: Api) -> None:
    """Register resources with the given Api."""
    # from students.py
    api.add_resource(StudentsListResource, '/students/')
    api.add_resource(StudentResource, '/students/<int:id>')
    api.add_resource(CreateStudentResource, '/students/')
    # from groups.py
    api.add_resource(AllGroupsResource, '/groups/students')
    api.add_resource(GroupsOnRequestResource, '/groups/<int:num>/students')
    # from courses.py
    api.add_resource(CoursesAllResource, '/courses/')
    api.add_resource(CourseUpdateResource, '/courses/<int:id>')
    # from student-course.py
    api.add_resource(StudentsInCourseResource, '/courses/<string:course>/students/')
    api.add_resource(OneStudentCoursesResource, '/students/<int:id>/courses/')
    api.add_resource(StudentCourseResource, '/students/<int:id_student>/courses/<int:id_course>')

    logger.info("--Registration of all URLs as API resources completed--")


def create_app(config_name: str) -> Flask:
    """Create a Flask src using the provided configuration name."""
    app = Flask(__name__)

    config_module = import_module(f'config.{config_name}')
    app.config.from_object(config_module)

    Limiter(app)
    logger.add('api_logs.json', colorize=True, format='{time} {level} {message}',
               level='DEBUG', rotation='10 days', retention="30 days", serialize=True)
    logger.info(f"Creating a Flask app in the 'app factory' using configuration: {config_name}!")

    db.init_app(app)
    # Migrate(db)
    api = Api(app, prefix='/api/v1')
    Swagger(app, template_file='swagger/swagger.yml')
    register_resources(api)

    @app.route('/')
    def index():
        """Redirect to API documentation for developers."""
        logger.info("--Redirecting from '/' to API documentation for developers--")
        return redirect(url_for('flasgger.apidocs', _external=True))

    return app


if __name__ == "__main__":
    app = create_app('production')
    # app = create_app('development')
    app.run()
