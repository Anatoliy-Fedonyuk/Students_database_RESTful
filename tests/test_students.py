"""In this module, we test endpoints and exceptions from the view <students.py>"""
import pytest

PAGE_DEF = 1
PER_PAGE_DEF = 10
PER_PAGE_CUST = 20
PAGE_CUST = 5
STUDENT = 1  # We assume that such ID exists.
STUDENT_NOT_EXIST = 999999


def test_students_list_resource_default(client):
    """Test to get a list of students with default parameters"""
    response = client.get('/api/v1/students/')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    data = response.get_json()[0]
    assert isinstance(data, dict)
    assert 'total_pages' in data and 'total_items' in data
    assert data['current_page'] == PAGE_DEF
    assert data['per_page'] == PER_PAGE_DEF
    students = data['students']
    assert isinstance(students, list)
    assert len(students) == PER_PAGE_DEF
    expected_keys = ['id', 'first_name', 'last_name', 'age', 'group_id']
    assert len(students[0]) == len(expected_keys)
    assert all((key in expected_keys for key in student) for student in students)


def test_students_list_resource_custom_params(client):
    """Test to get a list of students with custom parameters"""
    params = {'page': PAGE_CUST, 'per_page': PER_PAGE_CUST, 'sort': 'desc'}
    response = client.get('/api/v1/students/', query_string=params)
    assert response.status_code == 200
    data = response.get_json()[0]
    assert isinstance(data, dict)
    assert 'total_pages' in data and 'total_items' in data
    assert data['current_page'] == PAGE_CUST
    assert data['per_page'] == PER_PAGE_CUST
    students = data['students']
    assert isinstance(students, list)
    assert len(students) == PER_PAGE_CUST
    expected_keys = ['id', 'first_name', 'last_name', 'age', 'group_id']
    assert len(students[0]) == len(expected_keys)
    assert all((key in expected_keys for key in student) for student in students)


def test_students_list_resource_invalid_sort(client):
    """Test with invalid query parameters sort"""
    params = {'sort': 'invalid_sort'}  # Invalid sort option.

    response = client.get('/api/v1/students/', query_string=params)
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    data = response.get_json()
    assert isinstance(data, dict)
    assert 'error' in data
    assert data['error'][0]['ctx'] == {'Validation Error': 'Not allowed value'}


def test_students_list_resource_invalid_params(client):
    """Test with invalid query parameters"""
    params = {'page': -1, 'per_page': 50}
    response = client.get('/api/v1/students/', query_string=params)
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    data = response.get_json()
    assert isinstance(data, dict)
    assert 'error' in data


def test_student_resource_valid_id(client):
    """Test to get a student by the correct ID"""
    student_id = STUDENT
    response = client.get(f'/api/v1/students/{student_id}')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    data = response.get_json()
    assert isinstance(data, dict)
    expected_keys = ['id', 'first_name', 'last_name', 'age', 'group_id']
    assert len(data) == len(expected_keys)
    assert all(key in expected_keys for key in data)


def test_student_resource_invalid_id(client):
    """Test to get a student by incorrect ID (student does not exist)"""
    student_id = STUDENT_NOT_EXIST
    response = client.get(f'/api/v1/students/{student_id}')
    assert response.status_code == 404
    assert response.headers['Content-Type'] == 'application/json'
    data = response.get_json()
    assert isinstance(data, dict)
    assert 'error' in data
    assert data['error'] == f'Student with id={student_id} not found!'


def test_create_student_resource_valid_data(client):
    """Create a new student (POST) test with correct data"""
    new_st = {'first_name': 'John',
              'last_name': 'Doe',
              'age': 25,
              'group_id': 9}
    response = client.post('/api/v1/students/', json=new_st)
    assert response.status_code == 201
    assert response.headers['Content-Type'] == 'application/json'
    data = response.get_json()
    assert isinstance(data, dict)
    assert 'message' in data
    assert data['message'] == f'--Student {new_st["first_name"]} {new_st["last_name"]} created successfully--'

    """And Test POST if student already exists"""
    response = client.post('/api/v1/students/', json=new_st)
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    data = response.get_json()
    assert isinstance(data, dict)
    assert 'error' in data
    assert data['error'] == f'Student {new_st["first_name"]} {new_st["last_name"]} already exists'


def test_create_student_resource_invalid_data(client):
    """Create a new student (POST) test with incorrect data"""
    invalid_student_data = {'first_name': 'Invalid',
                            'last_name': 'Student',
                            'age': 10,  # Invalid age
                            'group_id': 2}
    response = client.post('/api/v1/students/', json=invalid_student_data)
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    data = response.get_json()
    assert isinstance(data, dict)
    assert 'error' in data


def test_student_delete_existing(client):
    """Existing student deletion test"""
    student_id = STUDENT
    response = client.delete(f'/api/v1/students/{student_id}')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    data = response.get_json()
    assert isinstance(data, dict)
    assert 'message' in data
    assert data['message'] == f'--Student {student_id} deleted successfully--'


def test_student_delete_nonexistent(client):
    """Delete non-existent student test"""
    student_id = STUDENT_NOT_EXIST
    response = client.delete(f'/api/v1/students/{student_id}')
    assert response.status_code == 404
    assert response.headers['Content-Type'] == 'application/json'
    data = response.get_json()
    assert isinstance(data, dict)
    assert 'error' in data
    assert data['error'] == f'Student {student_id} not found!'


if __name__ == '__main__':
    pytest.main()
