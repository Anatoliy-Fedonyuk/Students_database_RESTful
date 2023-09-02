"""In this module, we test endpoints and exceptions from the view <courses.py>"""
import pytest

NUMBERS_COURSES = 10
COURSE_ID = 1
COURSE_NOT_EXIST = 9999


def test_courses_all_resource(client):
    """Test GET a list of all courses."""
    response = client.get('/api/v1/courses/')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data[0]) == len(['id', 'course', 'description'])
    assert len(data) == NUMBERS_COURSES
    assert all('id' in course and 'course' in course and 'description' in course for course in data)


def test_course_update_resource_valid_input(client):
    """Test update a course by ID (PUT)."""
    course_id = COURSE_ID
    new_course_data = {'id_course': course_id,
                       'course': 'Updated Course Name',
                       'description': 'Updated Course Description'}

    response = client.put(f'/api/v1/courses/{course_id}', json=new_course_data)
    assert response.status_code == 201
    assert response.headers['Content-Type'] == 'application/json'
    data = response.get_json()
    assert 'message' in data
    assert data['message'] == f'Course with id={course_id} updated successfully'


def test_course_update_resource_invalid_input(client):
    """Test update a course by ID (PUT). Conflict input"""
    course_id = COURSE_ID
    invalid_course_data = {'id_course': 2,  # Non-matching course ID
                           'course': 'Updated Course Name',
                           'description': 'Updated Course Description'}

    response = client.put(f'/api/v1/courses/{course_id}', json=invalid_course_data)
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Invalid data provided, <id> should by equals <id_course>'


def test_course_update_resource_nonexistent_course(client):
    """Test update a course by ID (PUT). Invalid course"""
    course_id = COURSE_NOT_EXIST  # Nonexistent course ID
    new_course_data = {'id_course': course_id,
                       'course': 'Updated Course Name',
                       'description': 'Updated Course Description'}

    response = client.put(f'/api/v1/courses/{course_id}', json=new_course_data)
    assert response.status_code == 404
    assert response.headers['Content-Type'] == 'application/json'
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == f'Course with id={course_id} not found'


def test_course_update_resource_validation_error(client):
    """Test update a course by ID (PUT). Validation error"""
    course_id = COURSE_ID
    new_course_data = {'id_course': course_id,
                       'course': 1234,
                       'description': True}

    response = client.put(f'/api/v1/courses/{course_id}', json=new_course_data)
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    data = response.get_json()
    assert 'error' in data


if __name__ == '__main__':
    pytest.main()
