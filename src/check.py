"""This module is for checking whether it is a new empty database, if so,
 then we create all models for the database and generate data for their correct filling."""
import logging
from sqlalchemy import inspect, func

from src.main import create_app
from src.models import db, main_models
from src.generator import generate_groups, generate_students, generate_courses, generate_student_course

logger = logging.getLogger(__name__)


def generate_data() -> None:
    """Generate valid data to populate an empty database"""
    try:
        generate_groups()
        generate_students()
        generate_courses()
        generate_student_course()
        logger.info("--Data generated successfully--")
        return None
    except Exception as ex:
        logger.error(f"Error while generating data: {ex}")
        raise


def check_tables() -> None:
    """In this function, all tasks of the module are performed"""
    with app.app_context():
        ins = inspect(db.engine)
        tables_exist = all(ins.has_table(tab) for tab in ['groups', 'students', 'courses', 'student_course'])
        if not tables_exist:
            main_models()
            generate_data()
            logger.info("--PostgreSQL connection closed--")
        else:
            logger.info("--The ORM-models for PostgreSQL already exist!!!--")
        logger.info(f"PostgreSQL version: {db.session.query(func.version()).scalar()}")
        return None


if __name__ == "__main__":
    app = create_app('development')
    check_tables()
