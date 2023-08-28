import pytest
from flask import url_for, Flask

from app.init import create_app, db
from app.check import check_tables


@pytest.fixture(scope='module')
def app():
    app = create_app('testing')  # Используй тестовую конфигурацию
    with app.app_context():
        check_tables()  # Заполнение БД данными
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='module')
def client(app):
    return app.test_client()


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
