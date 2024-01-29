import pytest
from flask import url_for, session, Flask
from flask.testing import FlaskClient

def test_login(client):
    response = client.get(url_for('auth_routes.login'))
    assert response.status_code == 200
    assert b'Login' in response.data

def test_login_with_valid_credentials(client):
    response = client.post(url_for('auth_routes.login'), data={'username': 'validuser', 'password': 'validpassword'})
    assert response.status_code == 302  # Assuming you're using redirect on successful login
    assert session.get('user_id') is not None
    assert b'Login successful!' in client.get(response.headers['Location']).data

def test_login_with_invalid_credentials(client):
    response = client.post(url_for('auth_routes.login'), data={'username': 'invaliduser', 'password': 'invalidpassword'})
    assert response.status_code == 200
    assert b'Login Disabled: Log in with Github' in response.data

def test_initiate_github_oauth(client):
    response = client.get(url_for('auth_routes.initiate_github_oauth'))
    assert response.status_code == 302  # Assuming you're using redirect for GitHub OAuth initiation

def test_github_authorized(client, monkeypatch):
    # Mock the GitHub OAuth response
    def mock_authorized_response(*args, **kwargs):
        return {'access_token': 'mock_access_token'}

    monkeypatch.setattr('your_app.auth_routes.github.authorized_response', mock_authorized_response)

    # Simulate GitHub OAuth callback
    response = client.get(url_for('auth_routes.github_authorized'))
    assert response.status_code == 302  # Assuming you're using redirect after GitHub OAuth
    assert session.get('github_token') == ('mock_access_token', '')

def test_logout(client):
    response = client.get(url_for('auth_routes.logout'))
    assert response.status_code == 302  # Assuming you're using redirect after logout
    assert 'user_id' not in session
    assert 'github_user' not in session
    assert 'github_token' not in session
