"""---This module defines the Groups resources for the API.---"""
from flask import jsonify, Response
from flask_restful import Resource, abort
from sqlalchemy import func
from loguru import logger

from src.generator import db, Groups, Students

MIN_GROUP = 10
MAX_GROUP = 30


class AllGroupsResource(Resource):
    """--Resource for retrieving all groups and their student counts.--"""

    def get(self) -> Response| tuple[dict, int]:
        """-Get a list of all groups and their student counts.-"""
        try:
            groups = (db.session.query(Groups.group_id, Groups.name, func.count(Students.id).label('student_count'))
                      .outerjoin(Students, Groups.group_id == Students.group_id)
                      .group_by(Groups.group_id)
                      .order_by(Groups.group_id)
                      .all())

            result = [{'id': id, 'group_name': name, 'student_count': count} for id, name, count in groups]
            return jsonify(result)
        except Exception as ex:
            logger.error(f"Error while retrieving all groups: {ex}")
            abort(500, error='An error occurred while retrieving all groups')


class GroupsOnRequestResource(Resource):
    """--Resource for retrieving groups with no more than a given number of students.--"""

    def get(self, num: int) -> Response | tuple[dict, int]:
        """-Get a list of groups with no more than the specified number of students.-"""
        try:
            if num > MAX_GROUP or num < MIN_GROUP:
                logger.error(f'Invalid number of student {num} in group(10-30)')
                abort(400, error=f'Invalid number of student {num} in group(10-30)')

            groups = (db.session.query(Groups.name, func.count(Students.id).label('student_count'))
                      .outerjoin(Students, Groups.group_id == Students.group_id)
                      .group_by(Groups.name)
                      .having(func.count(Students.id) <= num)
                      .order_by('student_count')
                      .all())

            if not groups:
                logger.error(f'Groups with no more than {num} students do not exist')
                abort(400, error=f'Groups with no more than {num} students do not exist')

            result = [{'group_name': name, 'student_count': count} for name, count in groups]
            return jsonify(result)
        except Exception as ex:
            logger.error(f"Error while retrieving groups with a specified number of students: {ex}")
            abort(500, error='An error occurred while retrieving groups..')
