"""Models SQLAlchemy for PostgreSQL database create on this module"""
from loguru import logger
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

db = SQLAlchemy()


class Groups(db.Model):
    """Create Groups model."""
    group_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self) -> str:
        return f"Group :{self.group_id}, {self.name}"


class Students(db.Model):
    """Create Students model."""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False, unique=True)
    age = db.Column(db.Integer, nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'), nullable=False)

    def __repr__(self) -> str:
        return f"Student :{self.id}, {self.first_name}, {self.last_name}, {self.age}, {self.group_id}"


class Courses(db.Model):
    """Create Courses model."""
    id_course = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(150), nullable=False)

    def __repr__(self) -> str:
        return f"Course :{self.id_course}, {self.course}, {self.description}"


class StudentCourse(db.Model):
    """Create an associative model Student-Course."""
    id_student = db.Column(db.Integer, db.ForeignKey('students.id'), primary_key=True, nullable=False)
    id_course = db.Column(db.Integer, db.ForeignKey('courses.id_course'), primary_key=True, nullable=False)
    __table_args__ = (db.UniqueConstraint('id_student', 'id_course', name='_student_course_uc'),)

    def __repr__(self) -> str:
        return f"Student&Course : {self.id_student}, {self.id_course}"


def create_tables() -> None:
    """Create all models/tables in the PostgreSQL database."""
    try:
        with db.session.begin():
            logger.info("--PostgreSQL connection opened--")
            db.create_all()
            logger.info("--Tables created correct--")
        return None
    except SQLAlchemyError as ex:
        logger.error(f"Error while creating tables: {ex}")
        raise


def main_models() -> None:
    """Main function for creating SQLAlchemy models."""
    try:
        create_tables()
        logger.info("--Models SQLAlchemy created successfully--")
    except Exception as ex:
        logger.error(f"Error while working with PostgreSQL: {ex}")
        raise
    finally:
        db.session.close()
        logger.info("--SQLAlchemy session closed--")
        return None
