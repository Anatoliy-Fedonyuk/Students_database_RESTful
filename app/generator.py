from faker import Faker

from models import db, Groups, Students, Courses, StudentCourse
from app import app

faker = Faker()


def gen_data_group():
    for _ in range(10):
        name = faker.bothify(text='??-##')
        print(name, type(name))
        groups = Groups(name=name)
        db.session.add(groups)
    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        gen_data_group()
