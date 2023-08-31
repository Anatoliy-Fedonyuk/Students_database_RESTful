import pytest

NUMBERS_GROUPS = 10


def test_all_groups_resource(client):
    response = client.get('/api/v1/groups/students')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    expected_keys = ['group_name', 'id', 'student_count']
    assert len(data[-1]) == len(expected_keys)
    assert len(data) == NUMBERS_GROUPS
    assert all(key in data[-1] for key in expected_keys)


def test_groups_on_request_resource_valid_num(client):
    response = client.get('/api/v1/groups/25/students')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    expected_keys = ['group_name', 'student_count']
    assert len(data[0]) == len(expected_keys)
    assert all(key in data[0] for key in expected_keys)


def test_groups_on_request_resource_invalid_num(client):
    response = client.get('/api/v1/groups/5/students')
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Invalid number of student 5 in group(10-30)'


def test_groups_on_request_resource_max_num(client):
    response = client.get('/api/v1/groups/50/students')
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Invalid number of student 50 in group(10-30)'


if __name__ == '__main__':
    pytest.main()
