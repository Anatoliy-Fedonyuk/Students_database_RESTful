class ProductionConfig:
    FLASK_APP = 'app.init:create_app("development")'
    FLASK_ENV = 'production'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@127.0.0.1/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
