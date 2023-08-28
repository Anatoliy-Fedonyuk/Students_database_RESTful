# import os
# import sys
#
# # Получаем абсолютный путь до текущей директории
# current_dir = os.path.dirname(os.path.abspath(__file__))
#
# # Получаем абсолютный путь до родительской директории проекта
# project_dir = os.path.join(current_dir, '..')
#
# # Добавляем родительскую директорию в PYTHONPATH
# sys.path.insert(0, project_dir)
#
# PYTHONPATH = 'C:/Users/HP/Desktop/Projects Fox/Task 10 - SQL/'
# os.environ['PYTHONPATH'] = PYTHONPATH

FLASK_ENV = 'testing'
TESTING = True
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'postgresql://test:test@127.0.0.1/test'
SQLALCHEMY_TRACK_MODIFICATIONS = False