from flask import Flask
from flask_restful import Api
from importlib import import_module


def create_app(config_name):
    app = Flask(__name__)

    config_module = import_module(f'config.{config_name}')
    app.config.from_object(config_module)

    api = Api(app, prefix='/api/v1')

    # from views.students import StudentsListResource, StudentResource, StudentExistenceResource, CreateStudentResource
    def import_students_resources():
        from views.students import StudentsListResource, StudentResource, StudentExistenceResource, \
            CreateStudentResource
        return StudentsListResource, StudentResource, StudentExistenceResource, CreateStudentResource

    StudentsListResource, StudentResource, StudentExistenceResource, CreateStudentResource = import_students_resources()

    # Здесь продолжайте использовать эти классы как обычно

    api.add_resource(StudentsListResource, '/students')
    api.add_resource(StudentResource, '/students/<int:id>')
    api.add_resource(StudentExistenceResource, '/students/<int:id>/existence')
    api.add_resource(CreateStudentResource, '/students')

    return app


if __name__ == "__main__":
    create_app('development')
