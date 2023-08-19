from flask import jsonify, request
from flask_restful import Resource

from app.generator import db, Courses


class CoursesAllResource(Resource):
    def get(self):
        courses = Courses.query.all()

        courses.sort(key=lambda course: course.id_course)

        courses_data = [{'id': course.id_course, 'course': course.course, 'description': course.description}
                        for course in courses]

        return jsonify(courses_data)


class CourseUpdateResource(Resource):
    def put(self, id):
        course = Courses.query.get(id)
        if course:
            data = request.get_json()
            if data and all(i in data for i in ['course', 'description', 'id_course']):
                course.course = data.get('course', course.course)
                course.description = data.get('description', course.description)
                db.session.commit()
                return {'message': f'Course with id={id} updated successfully'}, 201
            else:
                return {'error': 'Invalid data provided'}, 400
        else:
            return {'error': f'Course with id={id} not found'}, 404
