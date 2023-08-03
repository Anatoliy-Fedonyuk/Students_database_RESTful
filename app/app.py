from flask import Flask

from models import db, main
from config import host, user, password, db_name

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


def check_tables():
    # Проверим, существуют ли таблицы
    tables_exist = db.engine.dialect.has_table(db.engine, 'group') and \
                   db.engine.dialect.has_table(db.engine, 'student') and \
                   db.engine.dialect.has_table(db.engine, 'course') and \
                   db.engine.dialect.has_table(db.engine, 'student_course')

    if not tables_exist:
        main()


if __name__ == "__main__":
    check_tables()
