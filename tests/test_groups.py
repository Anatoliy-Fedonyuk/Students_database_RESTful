"""In this module, we test endpoints and exceptions from the view <groups.py>"""
import pytest

NUMBERS_GROUPS = 10
MIN_GROUP = 5
MAX_GROUP = 50


def test_index_redirect(client):
    """Test redirect from end-point '/' to swagger"""
    response = client.get('/')
    assert response.status_code == 302
    assert '/' in response.headers['Location']


def test_all_groups_resource(client):
    """Test GET a list of all groups and their student counts."""
    response = client.get('/api/v1/groups/students')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    data = response.get_json()
    assert isinstance(data, list)
    expected_keys = ['group_name', 'id', 'student_count']
    assert len(data[-1]) == len(expected_keys)
    assert len(data) == NUMBERS_GROUPS
    assert all((key in expected_keys for key in group) for group in data)


def test_groups_on_request_resource_valid_num(client):
    """Test GET a list of groups with no more than the specified number of students"""
    response = client.get('/api/v1/groups/25/students')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    data = response.get_json()
    assert isinstance(data, list)
    expected_keys = ['group_name', 'student_count']
    assert len(data[0]) == len(expected_keys)
    assert all((key in expected_keys for key in group) for group in data)


def test_groups_on_request_resource_invalid_num(client):
    """Test GET a list of groups with no more than the specified number of students(invalid ID)"""
    num = MIN_GROUP
    response = client.get(f'/api/v1/groups/{num}/students')
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == f'Invalid number of student {num} in group(10-30)'


def test_groups_on_request_resource_max_num(client):
    """Test GET a list of groups with no more than the specified number of students(invalid ID)"""
    num = MAX_GROUP
    response = client.get(f'/api/v1/groups/{num}/students')
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == f'Invalid number of student {num} in group(10-30)'


if __name__ == '__main__':
    pytest.main()
