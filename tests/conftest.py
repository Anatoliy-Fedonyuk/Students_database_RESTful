"""This configuration file is for tests. He creates fixtures and get some tests."""
import pytest
from flask import Flask
from loguru import logger

from src.main import create_app, db
from src.check import generate_data


@pytest.fixture(scope='session')
def app():
    """Creating a flask application fixture."""
    app = create_app(config_name='testing')
    with app.app_context():
        db.create_all()
        generate_data()
        yield app
        db.session.remove()
        db.drop_all()
        logger.debug("---TEST SQLAlchemy session remove and DB dropped---")


@pytest.fixture(scope='session')
def client(app):
    """Creating a test client fixture."""
    return app.test_client()


def test_create_app(app):
    """Test correct create a flask application fixture"""
    assert isinstance(app, Flask)
    assert app.config['TESTING'] == True


def test_register_resources(app):
    """Test registration all end-points"""
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


if __name__ == '__main__':
    pytest.main()
