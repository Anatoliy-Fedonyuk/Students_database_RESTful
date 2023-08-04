from flask import Flask
from sqlalchemy import inspect
from models import db, main

from config_db import host, user, password, db_name

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


def check_tables():
    with app.app_context():
        ins = inspect(db.engine)
        tables_exist = all(ins.has_table(tab) for tab in ['groups', 'students', 'courses', 'student_course'])
        if not tables_exist:
            main()


# Далее тут будет описано взаимодействие с енд-поинтами по RESTfull api


if __name__ == "__main__":
    check_tables()
    app.run(debug=True)
