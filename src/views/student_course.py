"""---This module defines the StudentCourses resources for the API.---"""

from flask import jsonify, Response
from flask_restful import Resource

from src.generator import db, Students, Courses, StudentCourse

MIN, MAX = 1, 10


class StudentsInCourseResource(Resource):
    """Resource for retrieving students in a specific course."""

    def get(self, course: str) -> Response | tuple[dict, int]:
        """Get a list of students in a specific course."""
        course_exist = Courses.query.filter_by(course=course).first()
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
    """Resource for retrieving courses of a specific student."""

    def get(self, id: int) -> Response | tuple[dict, int]:
        """Get a list of courses for a specific student."""

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
            return {'error': f'Student with {id} not found'}, 404


def validate_student_and_course(id_student: int, id_course: int):
    """Course and student validation. """
    if id_course > MAX or id_course < MIN:
        return {'error': f'Invalid  {id_course=} (1-10)'}, 400

    student = Students.query.get(id_student)
    course = Courses.query.get(id_course)

    if not student or not course:
        return {'error': f'Student {id_student} or course {id_course} not found'}, 404

    return StudentCourse.query.filter_by(id_student=id_student, id_course=id_course).first()


class StudentCourseResource(Resource):
    """Resource for managing students in a course."""

    def post(self, id_student: int, id_course: int) -> tuple[dict, int]:
        """Add a student to a course (POST)."""
        student_course = validate_student_and_course(id_student, id_course)
        if student_course:
            return {'error': f'Student-course {id_student}-{id_course} association already exist'}, 400

        new_student_course = StudentCourse(id_student=id_student, id_course=id_course)
        db.session.add(new_student_course)
        db.session.commit()
        return {'message': f'Student {id_student} added to the course {id_course} successfully'}, 201

    def delete(self, id_student: int, id_course: int) -> tuple[dict, int]:
        """Remove a student from a course (DELETE)."""
        student_course = validate_student_and_course(id_student, id_course)
        if not student_course:
            return {'error': f'Student-course {id_student}-{id_course}  association not found'}, 404

        db.session.delete(student_course)
        db.session.commit()
        return {'message': f'Student {id_student} removed from the course {id_course} successfully'}, 200
