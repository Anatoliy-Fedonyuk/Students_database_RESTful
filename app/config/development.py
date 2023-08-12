# host = "127.0.0.1"
# user = "postgres"
# password = "postgres"
# db_name = "postgres"
# port = "5432"

FLASK_APP = ..app.py
FLASK_DEBUG = True
DEBUG = True
SQLALCHEMY_DATABASE_URI = f'postgresql://{user}:{password}@{host}/{db_name}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
