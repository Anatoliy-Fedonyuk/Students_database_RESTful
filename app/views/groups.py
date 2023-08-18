from flask import request, jsonify
from flask_restful import Resource
from sqlalchemy import func

from app.generator import db, Groups, Students


class AllGroupsResource(Resource):
    def get(self):
        groups = (db.session.query(Groups.group_id, Groups.name, func.count(Students.id).label('student_count'))
                  .outerjoin(Students, Groups.group_id == Students.group_id)
                  .group_by(Groups.group_id).all())

        groups.sort(key=Groups.group_id)

        result = [{'id': id, 'group_name': name, 'student_count': count} for id, name, count in groups]

        return jsonify(result)

class GroupsOnRequestResource(Resource):
    def get(self, num):
        groups = (db.session.query(Groups.name, func.count(Students.id).label('student_count'))
                  .outerjoin(Students, Groups.group_id == Students.group_id)
                  .group_by(Groups.name)
                  .having(func.count(Students.id) >= num)
                  .all())

        groups.sort(key=lambda group: group.student_count)

        result = [{'group_name': name, 'student_count': count} for name, count in groups]

        return jsonify(result)