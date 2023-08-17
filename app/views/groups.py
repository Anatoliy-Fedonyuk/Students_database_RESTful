from flask import request, jsonify
from flask_restful import Resource

from app.generator import db, Groups, Students

api.add_resource(GroupsListResource, '/groups/students/')


class GroupsListResource(Resource):
    def get(self):
        students = db.session.query.from_(Groups).left_join(Students).on(Groups.group_id = Students.group_id).groupby(
            Groups.name).select(Groups.name, function.Count(Students.id).as_('number of students'))

        students_data = [{'name': group.name, 'number of students': student.first_name,
                          'last_name': student.last_name, 'age': student.age,
                          'group_id': student.group_id} for student in students]
        return jsonify(students_data)
