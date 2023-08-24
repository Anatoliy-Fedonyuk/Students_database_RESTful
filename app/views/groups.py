"""---This module defines the Groups resources for the API.---"""

from flask import jsonify, Response
from flask_restful import Resource
from sqlalchemy import func

from app.generator import db, Groups, Students

MIN_GROUP = 10
MAX_GROUP = 30

class AllGroupsResource(Resource):
    """--Resource for retrieving all groups and their student counts.--"""

    def get(self) -> Response:
        """-Get a list of all groups and their student counts.-"""
        groups = (db.session.query(Groups.group_id, Groups.name, func.count(Students.id).label('student_count'))
                  .outerjoin(Students, Groups.group_id == Students.group_id)
                  .group_by(Groups.group_id)
                  .all())

        groups.sort(key=lambda group: group.group_id)

        result = [{'id': id, 'group_name': name, 'student_count': count} for id, name, count in groups]

        return jsonify(result)


class GroupsOnRequestResource(Resource):
    """--Resource for retrieving groups with no more than a given number of students.--"""

    def get(self, num: int) -> Response | tuple[dict, int]:
        """-Get a list of groups with no more than the specified number of students.-"""
        if num > MAX_GROUP or num < MIN_GROUP:
            return {'error': f'Invalid number of student {num} in group(10-30)'}, 400

        groups = (db.session.query(Groups.name, func.count(Students.id).label('student_count'))
                  .outerjoin(Students, Groups.group_id == Students.group_id)
                  .group_by(Groups.name)
                  .having(func.count(Students.id) <= num)
                  .all())

        if not groups:
            return {'error': f'Groups with no more than {num} students do not exist'}, 400

        groups.sort(key=lambda group: group.student_count)

        result = [{'group_name': name, 'student_count': count} for name, count in groups]

        return jsonify(result)
