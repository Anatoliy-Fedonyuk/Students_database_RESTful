"""---This module defines the Students resources for the API.---"""
from flask import request, jsonify
from flask_restful import Resource
from pydantic import BaseModel, PositiveInt, Field, ValidationError
from random import randint

from app.generator import db, Students, StudentCourse


class StudentsListResource(Resource):
    """--Resource for retrieving a paginated List of students.--"""

    class QueryParams(BaseModel):
        """--Validation of Query parameters.--"""
        page: PositiveInt = Field(1, description="Page number")
        per_page: PositiveInt = Field(10, description="Items per page")
        sort: str = Field('asc', description="Sorting order(asc, desc, age or group)")

    def get(self):
        """-Get a paginated List of students.-"""
        try:
            params = self.QueryParams(**request.args)
        except ValidationError as e:
            return {'error': e.errors()}, 400

        students = Students.query
        if params.sort == 'desc':
            students = students.order_by(Students.id.desc())
        elif params.sort == 'age':
            students = students.order_by(Students.age)
        elif params.sort == 'group':
            students = students.order_by(Students.group_id)
        else:
            students = students.order_by(Students.id)

        students_paging = students.paginate(page=params.page, per_page=params.per_page)

        students_data = [{'id': student.id, 'first_name': student.first_name,
                          'last_name': student.last_name, 'age': student.age,
                          'group_id': student.group_id} for student in students_paging.items]

        return {'students': students_data,
                'total_pages': students_paging.pages,
                'current_page': students_paging.page,
                'per_page': students_paging.per_page,
                'total_items': students_paging.total}


class StudentResource(Resource):
    """--Resource for retrieving and deleting a Student by ID.--"""

    def get(self, id):
        """-Get student by ID.-"""

        student = Students.query.get(id)
        if student:
            return jsonify({'id': student.id, 'first_name': student.first_name,
                            'last_name': student.last_name, 'age': student.age,
                            'group_id': student.group_id})
        else:
            return {'error': f'Student with id={id} not found'}, 404

    def delete(self, id):
        """-Delete student by ID (DELETE).-"""
        student = Students.query.get(id)
        if student:
            # Deleting related entries in student_course
            student_courses = StudentCourse.query.filter_by(id_student=student.id).all()
            for student_course in student_courses:
                db.session.delete(student_course)
            # Deleting a student by id
            db.session.delete(student)
            db.session.commit()
            return {'message': f'Student {id} deleted successfully'}, 200
        else:
            return {'error': f'Student {id} not found'}, 404


class CreateStudentResource(Resource):
    """--Resource for Creating a Student.--"""

    class RequestBody(BaseModel):
        """--Validation of Body parameters.--"""
        first_name: str = Field(..., description="First name of the student")
        last_name: str = Field(..., description="Last name of the student")
        age: int = Field(..., ge=15, le=60,description="Age of the student (15-60)")
        group_id: int = Field(None, ge=1, le=10,description="Group ID of the student (1-10)")

    def post(self):
        """-Create a new student (POST).-"""
        try:
            data = self.RequestBody(**request.get_json())
        except ValidationError as e:
            return {'error': e.errors()}, 400

        if not data.group_id:
            data.group_id = randint(1, 10)

        student = Students.query.filter_by(first_name=data.first_name,
                                           last_name=data.last_name,
                                           age=data.age).first()
        if student:
            return {'error': f'Student {data.first_name} {data.last_name} already exists'}, 400

        new_student = Students(first_name=data.first_name, last_name=data.last_name,
                               age=data.age, group_id=data.group_id)
        db.session.add(new_student)
        db.session.commit()

        return {'message': f'Student {data.first_name} {data.last_name} created successfully'}, 201
