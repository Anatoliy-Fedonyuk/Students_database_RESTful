"""---This module defines the Courses resources for the API.---"""

from flask import jsonify, request, Response
from flask_restful import Resource
from pydantic import BaseModel, Field

from src.generator import db, Courses


class CoursesAllResource(Resource):
    """Resource for retrieving all courses."""

    def get(self) -> Response:
        """Get a list of all courses."""
        courses = Courses.query.all()

        courses.sort(key=lambda course: course.id_course)

        courses_data = [{'id': course.id_course, 'course': course.course, 'description': course.description}
                        for course in courses]

        return jsonify(courses_data)


class CourseUpdateResource(Resource):
    """Resource for updating a course."""

    class RequestBody(BaseModel):
        """Validation of Body parameters."""
        id_course: int = Field(None, ge=1, le=10, description="Choice Course ID (1-10)")
        course: str = Field(..., description="Name of the course")
        description: str = Field(..., description="Description of the course")

    def put(self, id: int) -> tuple[dict, int]:
        """Update a course by ID (PUT)."""
        course = Courses.query.get(id)
        if course:
            data = self.RequestBody(**request.get_json())

            if id != data.id_course:
                return {'error': 'Invalid data provided, <id> should by equals <id_course>'}, 400

            if data:
                course.id_course = data.id_course
                course.course = data.course
                course.description = data.description
                db.session.commit()
                return {'message': f'Course with id={id} updated successfully'}, 201
            else:
                return {'error': 'Invalid data provided'}, 400

        else:
            return {'error': f'Course with id={id} not found'}, 404
