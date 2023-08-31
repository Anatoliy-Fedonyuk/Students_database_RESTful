import pytest
from flask import url_for, Flask

from src.main import create_app, db
from src.check import generate_data


@pytest.fixture(scope='session')
def app():
    app = create_app(config_name='testing')
    with app.app_context():
        db.create_all()
        generate_data()
        yield app
        db.session.remove()
        db.drop_all()
        print("[INFO] --SQLAlchemy session remove and DB dropped--")


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()


def test_create_app(app):
    assert isinstance(app, Flask)
    assert app.config['TESTING'] == True


def test_register_resources(app):
    with app.app_context():
        rules = [str(rule) for rule in app.url_map.iter_rules()]
        expected_rules = ['/',
                          '/api/v1/courses/',
                          '/api/v1/courses/<int:id>',
                          '/api/v1/courses/<string:course>/students/',
                          '/api/v1/groups/<int:num>/students',
                          '/api/v1/groups/students',
                          '/api/v1/students/',
                          '/api/v1/students/',
                          '/api/v1/students/<int:id>',
                          '/api/v1/students/<int:id>/courses/',
                          '/api/v1/students/<int:id_student>/courses/<int:id_course>']
        assert all(rule in rules for rule in expected_rules)


def test_index_redirect(client):
    response = client.get('/')
    assert response.status_code == 302
    assert '/' in response.headers['Location']


if __name__ == '__main__':
    pytest.main()
