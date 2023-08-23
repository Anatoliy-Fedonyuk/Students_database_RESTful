from flask import Flask
from flask_restful import Api
from importlib import import_module
# from flask_migrate import Migrate

from models import db
from views.students import StudentsListResource, StudentResource, CreateStudentResource
from views.groups import AllGroupsResource, GroupsOnRequestResource
from views.courses import CoursesAllResource, CourseUpdateResource
from views.student_course import (StudentsInCourseResource, AddStudentToCourseResource,
                                  RemoveStudentFromCourseResource, OneStudentCoursesResource)


def register_resources(api):
    api.add_resource(StudentsListResource, '/students/')
    api.add_resource(StudentResource, '/students/<int:id>')
    api.add_resource(CreateStudentResource, '/students/')

    api.add_resource(AllGroupsResource, '/groups/students')
    api.add_resource(GroupsOnRequestResource, '/groups/<int:num>/students')

    api.add_resource(CoursesAllResource, '/courses/')
    api.add_resource(CourseUpdateResource, '/courses/<int:id>')

    api.add_resource(StudentsInCourseResource, '/courses/<string:course>/students/')
    api.add_resource(OneStudentCoursesResource, '/students/<int:id>/courses/')
    api.add_resource(AddStudentToCourseResource, '/students/<int:id_student>/courses/<int:id_course>')
    api.add_resource(RemoveStudentFromCourseResource, '/students/<int:id_student>/courses/<int:id_course>')


def create_app(config_name):
    app = Flask(__name__)

    config_module = import_module(f'config.{config_name}')
    app.config.from_object(config_module)

    return app


app = create_app('development')
db.init_app(app)
# migrate = Migrate(app, db)
api = Api(app, prefix='/api/v1')
register_resources(api)

if __name__ == "__main__":
    app.run(debug=False)
