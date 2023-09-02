"""In this module, we test endpoints and exceptions from the view <student_course.py>"""
import pytest

from src.models import StudentCourse

COURSE_EXIST = "Music"  # We assume that such Course exists.
COURSE_NOT_EXIST = "NonExistentCourse"
STUDENT_EXIST = 1  # We assume that such ID exists.
STUDENT_NOT_EXIST = 999999
ID_COURSE = 1  # We assume that such ID Course exists.
ID_COURSE_NOT_EXIST = 777


def test_students_in_course_existing(client):
    """Test students on the course with valid data."""
    response = client.get(f'/api/v1/courses/{COURSE_EXIST}/students/')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    data = response.get_json()
    assert isinstance(data, list)
    expected_keys = ['course', 'first_name', 'last_name']
    assert len(data[0]) == len(expected_keys)
    assert all('course' in student and 'first_name' in student and 'last_name' in student for student in data)


def test_students_in_course_nonexistent(client):
    """Test students on the course with invalid data."""
    response = client.get(f'/api/v1/courses/{COURSE_NOT_EXIST}/students/')
    assert response.status_code == 404
    assert response.headers['Content-Type'] == 'application/json'
    data = response.get_json()
    assert isinstance(data, dict)
    assert 'error' in data
    assert data['error'] == f'There course-{COURSE_NOT_EXIST} not found'


def test_one_student_courses_existing(client):
    """Test student courses (valid data)"""
    id = STUDENT_EXIST
    response = client.get(f'/api/v1/students/{id}/courses/')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    data = response.get_json()
    assert isinstance(data, list)
    expected_keys = ['id', 'first_name', 'last_name', 'course']
    assert len(data[-1]) == len(expected_keys)
    assert all((key in expected_keys for key in course) for course in data)


def test_one_student_courses_nonexistent(client):
    """Test student courses (invalid data)"""
    id = STUDENT_NOT_EXIST
    response = client.get(f'/api/v1/students/{id}/courses/')
    assert response.status_code == 404
    assert response.headers['Content-Type'] == 'application/json'
    data = response.get_json()
    assert isinstance(data, dict)
    assert 'error' in data
    assert data['error'] == f'Student with {id} not found'


def test_student_course_create_success(client):
    """Student enrollment to a course test (valid data)"""
    id_student, id_course = STUDENT_EXIST, ID_COURSE
    #  Before creating a test, we check the existence of the association
    student_course = StudentCourse.query.filter_by(id_student=id_student, id_course=id_course).first()
    if student_course:
        pytest.skip(f"[INFO]Test skipped, because Student-course {id_student}-{id_course} association already exists")
    response = client.post(f'/api/v1/students/{id_student}/courses/{id_course}')
    assert response.status_code == 201
    assert response.headers['Content-Type'] == 'application/json'
    data = response.get_json()
    assert isinstance(data, dict)
    assert 'message' in data
    assert data['message'] == f'Student {id_student} added to the course {id_course} successfully'


def test_student_course_create_conflict(client):
    """Student enrollment to a course test (conflict data)"""
    id_student, id_course = STUDENT_EXIST, ID_COURSE
    response = client.post(f'/api/v1/students/{id_student}/courses/{id_course}')
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    data = response.get_json()
    assert isinstance(data, dict)
    assert 'error' in data
    assert data['error'] == f'Student-course {id_student}-{id_course} association already exist'


def test_student_course_create_invalid_student(client):
    """Student enrollment to a course test (invalid student)"""
    id_student, id_course = STUDENT_NOT_EXIST, ID_COURSE
    response = client.post(f'/api/v1/students/{id_student}/courses/{id_course}')
    assert response.status_code == 404
    assert response.headers['Content-Type'] == 'application/json'
    data = response.get_json()
    assert isinstance(data, dict)
    assert 'error' in data
    assert data['error'] == f'Student {id_student} or course {id_course} not found'


def test_student_course_delete_success(client):
    """Test remove a student from a course(DELETE with valid data)"""
    id_student, id_course = STUDENT_EXIST, ID_COURSE
    response = client.delete(f'/api/v1/students/{id_student}/courses/{id_course}')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    data = response.get_json()
    assert isinstance(data, dict)
    assert 'message' in data
    assert data['message'] == f'Student {id_student} removed from the course {id_course} successfully'


def test_student_course_create_invalid_course(client):
    """Test remove a student from a course (invalid Course)"""
    id_student, id_course = STUDENT_EXIST, ID_COURSE_NOT_EXIST
    response = client.delete(f'/api/v1/students/{id_student}/courses/{id_course}')
    assert response.status_code == 404
    assert response.headers['Content-Type'] == 'application/json'
    data = response.get_json()
    assert isinstance(data, dict)
    assert 'error' in data
    assert data['error'] == f'Student {id_student} or course {id_course} not found'


def test_student_course_delete_not_found(client):
    """Test remove a student from a course(association not found)"""
    id_student, id_course = STUDENT_EXIST, ID_COURSE
    response = client.delete(f'/api/v1/students/{id_student}/courses/{id_course}')
    assert response.status_code == 404
    assert response.headers['Content-Type'] == 'application/json'
    data = response.get_json()
    assert isinstance(data, dict)
    assert 'error' in data
    assert data['error'] == f'Student-course {id_student}-{id_course}  association not found'


if __name__ == '__main__':
    pytest.main()
