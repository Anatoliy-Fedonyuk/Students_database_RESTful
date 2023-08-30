import pytest
from flask import url_for, Flask

from app.main import create_app, db
# from app.models import db
from app.check import check_tables


@pytest.fixture(scope='module')
def app():
    app = create_app('testing')
    with app.app_context():
        yield app


@pytest.fixture(scope='module')
def client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture(scope='module')
def db(app):
    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()


def test_check_tables(app, client, db):
    with app.app_context():
        result = check_tables()
        assert "ORM-models PostgreSQL already exist" in result


def test_create_app(app):
    assert isinstance(app, Flask)
    assert app.config['TESTING'] == True


def test_register_resources(app):
    with app.app_context():
        api = app.extensions['restful'].api
        assert api.resources['/students/']
        assert api.resources['/students/<int:id>']
        assert api.resources['/groups/students']
        assert api.resources['/groups/<int:num>/students']
        assert api.resources['/courses/']
        assert api.resources['/courses/<int:id>']
        assert api.resources['/courses/<string:course>/students/']
        assert api.resources['/students/<int:id>/courses/']
        assert api.resources['/students/<int:id_student>/courses/<int:id_course>']


def test_index_redirect(client):
    response = client.get('/')
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/api/v1/apidocs/'


if __name__ == '__main__':
    pytest.main()
