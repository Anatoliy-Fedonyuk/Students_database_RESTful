FLASK_ENV = 'development'
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'postgresql://fedonyuk:74fedonyuk74@127.0.0.1/postgres01'
SQLALCHEMY_TRACK_MODIFICATIONS = False
# Enable API request rate limiting
API_RATE_LIMIT_ENABLED = True
API_RATE_LIMIT_WINDOW = '1 minute'
API_RATE_LIMIT_COUNT = 20
# Enable loging
LOG_LEVEL = 'DEBUG'
LOG_FILE = 'development.log'
