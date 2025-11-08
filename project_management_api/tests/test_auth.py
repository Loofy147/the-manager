import json

def test_register(client):
    response = client.post('/api/auth/register', data=json.dumps({
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password",
        "first_name": "Test",
        "last_name": "User"
    }), content_type='application/json')
    assert response.status_code == 201
    assert 'user' in response.json

def test_login(client):
    # First, register a user
    client.post('/api/auth/register', data=json.dumps({
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password",
        "first_name": "Test",
        "last_name": "User"
    }), content_type='application/json')

    # Now, log in
    response = client.post('/api/auth/login', data=json.dumps({
        "username_or_email": "testuser",
        "password": "password"
    }), content_type='application/json')
    assert response.status_code == 200
    assert 'token' in response.json
