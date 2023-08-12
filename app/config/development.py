from ..config_db import host, user, password, db_name

FLASK_APP = "app"
FLASK_DEBUG = True
DEBUG = True
SQLALCHEMY_DATABASE_URI = f'postgresql://{user}:{password}@{host}/{db_name}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
