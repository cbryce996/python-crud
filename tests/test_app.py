# tests/test_app.py
from src import app

import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Login" in response.data

def test_login_with_valid_credentials(client):
    response = client.post('/login', data={'username': 'test_user', 'password': 'test_password'})
    assert response.status_code == 200
    assert b"Successfully logged in" in response.data

def test_login_with_invalid_credentials(client):
    response = client.post('/login', data={'username': 'invalid_user', 'password': 'invalid_password'})
    assert response.status_code == 200
    assert b"Invalid credentials" in response.data
