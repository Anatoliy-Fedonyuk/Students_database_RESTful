from flask import jsonify, request
from flask_restful import Resource

from app.generator import db, Students, Courses, StudentCourse


class StudentsInCourseResource(Resource):
    def get(self, course):
        course_exist = Courses.query.filter_by(course=course).first()
        print(course_exist)
        if not course_exist:
            return {'error': f'There course-{course} not found'}, 404

        students = (db.session.query(Courses.course, Students.first_name, Students.last_name)
                    .outerjoin(StudentCourse, Courses.id_course == StudentCourse.id_course)
                    .outerjoin(Students, Students.id == StudentCourse.id_student)
                    .filter(Courses.course == course)
                    .all())

        result = [{'course': course, 'first_name': first_name,
                   'last_name': last_name} for course, first_name, last_name in students]
        return jsonify(result)


class OneStudentCoursesResource(Resource):
    def get(self, id):
        student = Students.query.get(id)
        if student:
            courses = (db.session.query(Students.id, Students.first_name, Students.last_name, Courses.course)
                       .outerjoin(StudentCourse, StudentCourse.id_student == Students.id)
                       .outerjoin(Courses, Courses.id_course == StudentCourse.id_course)
                       .filter(Students.id == id)
                       .all())

            res_query = [{'id': student.id, 'first_name': student.first_name,
                          'last_name': student.last_name, 'course': course.course} for course in courses]
            return jsonify(res_query)
        else:
            return {'error': f'Student {id} not found'}, 404


class AddStudentToCourseResource(Resource):
    def post(self, id_student, id_course):
        data = request.get_json()
        if not data or 'id_student' not in data or 'id_course' not in data:
            return {'error': 'Invalid input data'}, 400

        id_student = data.get('id_student')
        id_course = data.get('id_course')

        student = Students.query.get(id_student)
        course = Courses.query.get(id_course)

        if not student or not course:
            return {'error': f'Student {id_student} or course {id_course} not found'}, 404

        student_course = StudentCourse.query.filter_by(id_student=id_student, id_course=id_course).first()
        if student_course:
            return {'error': f'Student-course {id_student}-{id_course} association already exist'}, 400

        new_student_course = StudentCourse(id_student=id_student, id_course=id_course)
        db.session.add(new_student_course)
        db.session.commit()
        return {'message': f'Student {id_student} added to the course {id_course} successfully'}, 201


class RemoveStudentFromCourseResource(Resource):
    def delete(self, id_student, id_course):
        student = Students.query.get(id_student)
        course_exist = Courses.query.get(id_course)
        print(student)
        print(course_exist)
        if not student or not course_exist:
            return {'error': f'Student {id_student} or course {id_course} not found'}, 404

        student_course = StudentCourse.query.filter_by(id_student=id_student, id_course=id_course).first()
        if not student_course:
            return {'error': f'Student-course {id_student}-{id_course}  association not found'}, 404

        db.session.delete(student_course)
        db.session.commit()
        return {'message': f'Student {id_student} removed from the course {id_course} successfully'}, 200
