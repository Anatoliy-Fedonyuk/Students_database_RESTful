from flask import jsonify, request
from flask_restful import Resource

from app.generator import db, Students, Courses, StudentCourse


class StudentsInCourseResource(Resource):
    def get(self, course):
        students = (db.session.query(Courses.course, Students.first_name, Students.last_name, Students.id)
                    .outerjoin(StudentCourse, StudentCourse.id_course == Courses.id_course)
                    .outerjoin(Students, Students.id == StudentCourse.id_student)
                    .filter(Courses.course == course)
                    .all())
        print(students)

        result = [{'course': course.course, 'first_name': student.first_name, 'last_name': student.last_name,
                   'id': student.id} for student in students]
        print(result)

        return jsonify(result)


class OneStudentCoursesResource(Resource):
    def get(self, id):
        courses = (db.session.query(Students.first_name, Students.last_name, Courses.course)
                   .outerjoin(StudentCourse, StudentCourse.id_student == Students.id)
                   .outerjoin(Courses, Courses.id_course == StudentCourse.id_course)
                   .filter(Students.id == id)
                   .all())

        print(courses)
        res_query = [{'id': course.id, 'first_name': course.first_name,
                      'last_name': course.last_name, 'course': course.course} for course in courses]
        print(res_query)

        return jsonify(res_query)


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
