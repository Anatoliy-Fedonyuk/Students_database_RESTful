"""The main module of our FLASK RESTFUL API application - <SQL>"""
import sys
import os
from flask import Flask, redirect, url_for
from flask_restful import Api
from importlib import import_module
from flasgger import Swagger
# from flask_migrate import Migrate

from models import db
from views.students import StudentsListResource, StudentResource, CreateStudentResource
from views.groups import AllGroupsResource, GroupsOnRequestResource
from views.courses import CoursesAllResource, CourseUpdateResource
from views.student_course import StudentsInCourseResource, StudentCourseResource, OneStudentCoursesResource

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def register_resources(api: Api) -> None:
    """Register resources with the given Api."""
    api.add_resource(StudentsListResource, '/students/')
    api.add_resource(StudentResource, '/students/<int:id>')
    api.add_resource(CreateStudentResource, '/students/')

    api.add_resource(AllGroupsResource, '/groups/students')
    api.add_resource(GroupsOnRequestResource, '/groups/<int:num>/students')

    api.add_resource(CoursesAllResource, '/courses/')
    api.add_resource(CourseUpdateResource, '/courses/<int:id>')

    api.add_resource(StudentsInCourseResource, '/courses/<string:course>/students/')
    api.add_resource(OneStudentCoursesResource, '/students/<int:id>/courses/')
    api.add_resource(StudentCourseResource, '/students/<int:id_student>/courses/<int:id_course>')


def create_app(config_name: str) -> Flask:
    """Create a Flask app using the provided configuration name."""
    app = Flask(__name__)

    config_module = import_module(f'config.{config_name}')
    app.config.from_object(config_module)

    db.init_app(app)
    # migrate = Migrate(app, db)
    api = Api(app, prefix='/api/v1')
    register_resources(api)

    return app


app = create_app('development')
swagger = Swagger(app, template_file='swagger/swagger.yml')


@app.route('/')
def index():
    """Redirect to API documentation for developers."""
    return redirect(url_for('flasgger.apidocs', _external=True))


if __name__ == "__main__":
    app.run()
