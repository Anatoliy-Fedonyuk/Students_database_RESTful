from flask import jsonify, request
from flask_restful import Resource

from app.generator import db, Students, Courses, StudentCourse

class StudentsInCourseResource(Resource):
    def get(self, course):
        students = (db.session.query(Students)
                    .join(StudentCourse, Students.id == StudentCourse.id_student)
                    .join(Courses, StudentCourse.id_course == Courses.id_course)
                    .filter(Courses.course == course)
                    .all())

        result = [{'id': student.id, 'first_name': student.first_name,
                   'last_name': student.last_name, 'age': student.age,
                   'group_id': student.group_id} for student in students]

        return jsonify(result)

class OneStudentCoursesResource(Resource):
    def get(self):
        pass

class AddStudentToCourseResource(Resource):
    def post(self):
        data = request.get_json()
        if not data or 'student_id' not in data or 'course_id' not in data:
            return {'error': 'Invalid input data'}, 400

        student_id = data['student_id']
        course_id = data['course_id']

        student = Students.query.get(student_id)
        course = Courses.query.get(course_id)

        if not student or not course:
            return {'error': 'Student or course not found'}, 404

        new_student_course = StudentCourse(id_student=student_id, id_course=course_id)
        db.session.add(new_student_course)
        db.session.commit()

        return {'message': 'Student added to the course successfully'}, 201

class RemoveStudentFromCourseResource(Resource):
    def delete(self):
        data = request.get_json()
        if not data or 'student_id' not in data or 'course_id' not in data:
            return {'error': 'Invalid input data'}, 400

        student_id = data['student_id']
        course_id = data['course_id']

        student_course = StudentCourse.query.filter_by(id_student=student_id, id_course=course_id).first()

        if not student_course:
            return {'error': 'Student-course association not found'}, 404

        db.session.delete(student_course)
        db.session.commit()

        return {'message': 'Student removed from the course successfully'}, 204
