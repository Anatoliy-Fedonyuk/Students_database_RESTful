class TestingConfig:
    FLASK_APP = 'app:init'
    FLASK_ENV = 'testing'
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://test:test@127.0.0.1/test'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
