from flask import request, jsonify
from flask_restful import Resource
from sqlalchemy import func

from app.generator import db, Groups, Students


class AllGroupsResource(Resource):
    def get(self):
        groups = (db.session.query(Groups.name, func.count(Students.id).label('student_count'))
                  .outerjoin(Students, Groups.group_id == Students.group_id)
                  .group_by(Groups.name).all())

        groups.sort(key=lambda group: group.student_count)

        result = [{'group_name': group_name, 'student_count': student_count} for group_name, student_count in groups]

        return jsonify(result)
