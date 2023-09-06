"""---This module defines the Courses resources for the API.---"""
from flask import jsonify, request, Response
from flask_restful import Resource
from pydantic import BaseModel, Field, ValidationError
from loguru import logger

from src.generator import db, Courses


class CoursesAllResource(Resource):
    """Resource for retrieving all courses."""

    def get(self) -> Response | tuple[dict, int]:
        """Get a list of all courses."""
        try:
            courses = Courses.query.order_by(Courses.id_course).all()

            courses_data = [{'id': course.id_course, 'course': course.course, 'description': course.description}
                            for course in courses]
            return jsonify(courses_data)

        except Exception as ex:
            logger.error(f"Error while retrieving all courses: {ex}")
            return {'error': 'An error occurred while retrieving all courses'}, 500


class CourseUpdateResource(Resource):
    """Resource for updating a course."""

    class RequestBody(BaseModel):
        """Validation of Body parameters."""
        id_course: int = Field(..., ge=1, le=10, description="Choice Course ID (1-10)")
        course: str = Field(..., pattern=r'^[A-Z]{1}[a-z-]+$', description="Name of the course")
        description: str = Field(..., description="Description of the course")

    def put(self, id: int) -> tuple[dict, int]:
        """Update a course by ID (PUT)."""
        try:
            course = Courses.query.get(id)
            if course:
                data = self.RequestBody(**request.get_json())
                if id != data.id_course:
                    logger.error('Invalid data provided, <id> should be equal to <id_course>')
                    return {'error': 'Invalid data provided, <id> should by equals <id_course>'}, 400

                course.id_course = data.id_course
                course.course = data.course
                course.description = data.description
                db.session.commit()
                logger.info(f'Course with id={id} updated successfully')
                return {'message': f'Course with id={id} updated successfully'}, 201
            else:
                logger.error(f'Course with id={id} not found')
                return {'error': f'Course with id={id} not found'}, 404

        except ValidationError as exc:
            logger.error(f'Validation error: {exc.errors()}')
            return {'error': exc.errors()}, 400
        except Exception as ex:
            logger.error(f"Error while updating course with id={id}: {ex}")
            return {'error': f'An error occurred while updating the course id={id}'}, 500
