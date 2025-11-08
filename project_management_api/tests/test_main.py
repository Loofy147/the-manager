def test_get_users(client):
    response = client.get('/api/users')
    assert response.status_code == 200
    assert 'users' in response.json

def test_healthz(client):
    response = client.get('/healthz')
    assert response.status_code == 200
    assert b"OK" in response.data
