"""In this module, we test endpoints and exceptions from the view <students.py>"""
import pytest

PAGE_DEF = 1
PER_PAGE_DEF = 10
PER_PAGE_CUST = 20
PAGE_CUST = 2


def test_students_list_resource_default(client):
    """Test to get a list of students with default parameters"""
    response = client.get('/api/v1/students/')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    data = response.get_json()
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
    """Test for obtaining a list of students with custom parameters"""
    params = {'page': PAGE_CUST, 'per_page': PER_PAGE_CUST, 'sort': 'desc'}
    response = client.get('/api/v1/students/', query_string=params)
    assert response.status_code == 200
    data = response.get_json()
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


def test_students_list_resource_invalid_params(client):
    # Тест с невалидными параметрами запроса
    params = {
        'page': -1,  # Невалидная страница
        'per_page': 50,  # Превышено максимальное количество студентов на странице
        'sort': 'invalid_sort'  # Невалидный параметр сортировки
    }
    response = client.get('/api/v1/students/', query_string=params)
    assert response.status_code == 400
    data = response.get_json()
    assert isinstance(data, dict)
    assert 'error' in data
    assert 'page' in data['error']
    assert 'per_page' in data['error']
    assert 'sort' in data['error']


def test_student_resource_valid_id(client):
    # Тест получения студента по корректному ID
    student_id = 1  # Предполагаем, что студент с ID=1 существует
    response = client.get(f'/api/v1/students/{student_id}')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    data = response.get_json()
    assert isinstance(data, dict)
    assert 'id' in data
    assert 'first_name' in data
    assert 'last_name' in data
    assert 'age' in data
    assert 'group_id' in data


def test_student_resource_invalid_id(client):
    # Тест получения студента по некорректному ID (студент не существует)
    student_id = 9999  # Предполагаем, что студента с таким ID нет
    response = client.get(f'/api/v1/students/{student_id}')
    assert response.status_code == 404
    data = response.get_json()
    assert isinstance(data, dict)
    assert 'error' in data


def test_create_student_resource_valid_data(client):
    # Тест создания студента с корректными данными
    new_student_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'age': 25,
        'group_id': 5
    }
    response = client.post('/api/v1/students/', json=new_student_data)
    assert response.status_code == 201
    assert response.headers['Content-Type'] == 'application/json'
    data = response.get_json()
    assert isinstance(data, dict)
    assert 'message' in data


def test_create_student_resource_invalid_data(client):
    # Тест создания студента с некорректными данными (например, возраст вне диапазона)
    invalid_student_data = {
        'first_name': 'Invalid',
        'last_name': 'Student',
        'age': 10,  # Невалидный возраст
        'group_id': 2
    }
    response = client.post('/api/v1/students/', json=invalid_student_data)
    assert response.status_code == 400
    data = response.get_json()
    assert isinstance(data, dict)
    assert 'error' in data


if __name__ == '__main__':
    pytest.main()
