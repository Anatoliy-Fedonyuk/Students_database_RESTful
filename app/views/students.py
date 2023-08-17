from flask import request, jsonify
from flask_restful import Resource
from random import randint

from app.generator import db, Students, StudentCourse


class StudentsListResource(Resource):
    def get(self):
        sort_param = request.args.get('sort', 'asc')

        students = Students.query.all()

        if sort_param == 'desc':
            students.sort(key=lambda student: student.id, reverse=True)
        elif sort_param == 'age':
            students.sort(key=lambda student: student.age)
        elif sort_param == 'group':
            students.sort(key=lambda student: student.group_id)

        students_data = [{'id': student.id, 'first_name': student.first_name,
                          'last_name': student.last_name, 'age': student.age,
                          'group_id': student.group_id} for student in students]
        return jsonify(students_data)


class StudentResource(Resource):
    def get(self, id):
        student = Students.query.get(id)
        if student:
            return jsonify({'id': student.id, 'first_name': student.first_name,
                            'last_name': student.last_name, 'age': student.age,
                            'group_id': student.group_id})
        else:
            return {'error': 'Student not found'}, 404

    def delete(self, id):
        student = Students.query.get(id)
        if student:
            # Deleting related entries in student_course
            student_courses = StudentCourse.query.filter_by(id_student=student.id).all()
            for student_course in student_courses:
                db.session.delete(student_course)
            # Deleting a student by id
            db.session.delete(student)
            db.session.commit()
            return {'message': 'Student deleted successfully'}
        else:
            return {'error': 'Student not found'}, 404


class CreateStudentResource(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return {'error': 'No input data provided'}, 400

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        age = data.get('age')

        if not first_name or not last_name or not age:
            return {'error': 'Missing required fields'}, 400

        student = Students.query.filter_by(first_name=first_name, last_name=last_name, age=age).first()
        if student:
            return {'error': 'Student already exists'}, 400

        group_id = randint(1, 10)  # Выбираем случайный номер группы
        new_student = Students(first_name=first_name, last_name=last_name, age=age, group_id=group_id)
        db.session.add(new_student)
        db.session.commit()
        return {'message': 'Student created successfully'}, 201
