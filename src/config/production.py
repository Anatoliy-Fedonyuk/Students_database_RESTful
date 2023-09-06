FLASK_ENV = 'production'
DEBUG = False
SQLALCHEMY_DATABASE_URI = 'postgresql://fedonyuk:74fedonyuk74@127.0.0.1/postgres01'
SQLALCHEMY_TRACK_MODIFICATIONS = False
# Enable API request rate limiting
API_RATE_LIMIT_ENABLED = True
API_RATE_LIMIT_WINDOW = '1 minute'
API_RATE_LIMIT_COUNT = 20
# Enable loging
LOG_LEVEL = 'INFO'
LOG_FILE = 'production.log'
# Using Redis as a caching system
CACHE_TYPE = 'redis'  # Использование Redis как системы кэширования
CACHE_REDIS_URL = 'redis://localhost:6379/0'  # URL для подключения к Redis
CACHE_DEFAULT_TIMEOUT = 300  # Таймаут кэша по умолчанию (в секундах)
CACHE_KEY_PREFIX = 'myapp'  # Префикс ключей кэша
