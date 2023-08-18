from flask import Flask
from flask_restful import Api
from importlib import import_module

from models import db
from views.students import StudentsListResource, StudentResource, CreateStudentResource
from views.groups import AllGroupsResource, GroupsOnRequestResource
from views.courses import CoursesAllResource, CourseResource


def register_students_resources(api):
    api.add_resource(StudentsListResource, '/students/')
    api.add_resource(StudentResource, '/students/<int:id>')
    api.add_resource(CreateStudentResource, '/students/')


def register_groups_resources(api):
    api.add_resource(AllGroupsResource, '/groups/students')
    api.add_resource(GroupsOnRequestResource, '/groups/<int:num>/students')


def register_courses_resources(api):
    api.add_resource(CoursesAllResource, '/courses/')
    api.add_resource(CourseResource, '/courses/<int:id>')


def create_app(config_name):
    app = Flask(__name__)

    config_module = import_module(f'config.{config_name}')
    app.config.from_object(config_module)

    return app


app = create_app('development')
db.init_app(app)
api = Api(app, prefix='/api/v1')

register_students_resources(api)
register_groups_resources(api)
register_courses_resources(api)

if __name__ == "__main__":
    app.run(debug=False)
