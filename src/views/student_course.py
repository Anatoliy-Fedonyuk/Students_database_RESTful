"""---This module defines the StudentCourses resources for the API.---"""
from flask import jsonify, Response
from flask_restful import Resource
from loguru import logger

from src.generator import db, Students, Courses, StudentCourse

ERROR_NOT_FOUND = 'Error_not_found_flag'


class StudentsInCourseResource(Resource):
    """Resource for retrieving students in a specific course."""

    def get(self, course: str) -> Response | tuple[dict, int]:
        """Get a list of students in a specific course."""
        try:
            course_exist = Courses.query.filter_by(course=course).first()
            if not course_exist:
                logger.error(f"There course-{course} not found!")
                return {'error': f'There course-{course} not found!'}, 404

            students = (db.session.query(Courses.course, Students.first_name, Students.last_name)
                        .outerjoin(StudentCourse, Courses.id_course == StudentCourse.id_course)
                        .outerjoin(Students, Students.id == StudentCourse.id_student)
                        .filter(Courses.course == course)
                        .all())

            result = [{'course': course, 'first_name': first_name,
                       'last_name': last_name} for course, first_name, last_name in students]
            return jsonify(result)
        except Exception as e:
            logger.error(f"An error occurred while retrieving students in course: {e}")
            return {'error': 'An error occurred while retrieving students in course'}, 500


class OneStudentCoursesResource(Resource):
    """Resource for retrieving courses of a specific student."""

    def get(self, id: int) -> Response | tuple[dict, int]:
        """Get a list of courses for a specific student."""
        try:
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
                logger.error(f"Student with id={id} not found")
                return {'error': f'Student with {id} not found!'}, 404
        except Exception as ex:
            logger.error(f"An error occurred while retrieving student courses: {ex}")
            return {'error': 'An error occurred while retrieving student courses'}, 500


def validate_student_and_course(id_student: int, id_course: int):
    """Course and student validation. """
    student = Students.query.get(id_student)
    course = Courses.query.get(id_course)
    if not student or not course:
        return ERROR_NOT_FOUND
    return StudentCourse.query.filter_by(id_student=id_student, id_course=id_course).first()


class StudentCourseResource(Resource):
    """Resource for managing students in a course."""

    def post(self, id_student: int, id_course: int) -> tuple[dict, int]:
        """Add a student to a course (POST)."""
        try:
            student_course = validate_student_and_course(id_student, id_course)
            if not student_course:
                new_student_course = StudentCourse(id_student=id_student, id_course=id_course)
                db.session.add(new_student_course)
                db.session.commit()
                logger.info(f'--Student {id_student} added to the course {id_course} successfully--')
                return {'message': f'--Student {id_student} added to the course {id_course} successfully--'}, 201

            if student_course == ERROR_NOT_FOUND:
                logger.error(f'Student {id_student} or course {id_course} not found!')
                return {'error': f'Student {id_student} or course {id_course} not found!'}, 404
            else:
                logger.error(f'Student-course {id_student}-{id_course} association already exist!')
                return {'error': f'Student-course {id_student}-{id_course} association already exist!'}, 400
        except Exception as e:
            logger.error(f"An error occurred while adding a student to a course: {e}")
            return {'error': 'An error occurred while adding a student to a course'}, 500

    def delete(self, id_student: int, id_course: int) -> tuple[dict, int]:
        """Remove a student from a course (DELETE)."""
        try:
            student_course = validate_student_and_course(id_student, id_course)
            if not student_course:
                logger.error(f'Student-course {id_student}-{id_course}  association not found!')
                return {'error': f'Student-course {id_student}-{id_course}  association not found!'}, 404
            elif student_course == ERROR_NOT_FOUND:
                logger.error(f'Student {id_student} or course {id_course} not found!')
                return {'error': f'Student {id_student} or course {id_course} not found!'}, 404
            else:
                db.session.delete(student_course)
                db.session.commit()
                logger.info(f'--Student {id_student} removed from the course {id_course} successfully--')
                return {'message': f'--Student {id_student} removed from the course {id_course} successfully--'}, 200
        except Exception as ex:
            logger.error(f"An error occurred while removing a student from a course: {ex}")
            return {'error': 'An error occurred while removing a student from a course'}, 500
