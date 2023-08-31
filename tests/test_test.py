import pytest
from flask import Flask
# from flask_restful import Api
from src.main import create_app


@pytest.fixture(scope='module')
def app():
    app = create_app('testing')
    return app


@pytest.fixture(scope='module')
def client(app):
    return app.test_client()


@pytest.fixture(scope='module')
def api(app):
    with app.app_context():
        yield app.extensions['restful'].api


def test_create_app(app):
    assert isinstance(app, Flask)
    assert app.config['TESTING'] == True


def test_register_resources(app, api):
    with app.app_context():
        assert api.resources['/api/v1/students/']
        assert api.resources['/api/v1/students/<int:id>']
        assert api.resources['/api/v1/groups/students']
        assert api.resources['/api/v1/groups/<int:num>/students']
        assert api.resources['/api/v1/courses/']
        assert api.resources['/api/v1/courses/<int:id>']
        assert api.resources['/api/v1/courses/<string:course>/students/']
        assert api.resources['/api/v1/students/<int:id>/courses/']
        assert api.resources['/api/v1/students/<int:id_student>/courses/<int:id_course>']


def test_index_redirect(client):
    response = client.get('/')
    assert response.status_code == 302
    assert '/api/v1/apidocs/' in response.headers['Location']


if __name__ == '__main__':
    pytest.main()
