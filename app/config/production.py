from ..config_db import host, user, password, db_name

DEBUG = True
SQLALCHEMY_DATABASE_URI = f'postgresql://{user}:{password}@{host}/{db_name}'
SQLALCHEMY_TRACK_MODIFICATIONS = False