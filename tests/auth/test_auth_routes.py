from unittest.mock import patch
from flask import Flask, session
from app.routes import auth_routes

def test_github_oauth_redirect(client):
    response = client.get('/auth/oauth/login')
    assert response.status_code == 302  # Expecting a redirect

def test_github_oauth_callback(client, monkeypatch):
    with client.session_transaction() as sess:
        sess['github_token'] = ('mock_access_token', '')

    response = client.get('/auth/oauth/callback')
    assert response.status_code == 302  # Expecting a redirect

def test_github_oauth_callback(client):
    # Mock the GitHub OAuth response
    mock_resp = {'access_token': 'mock_access_token', 'user': {'login': 'mock_user'}}
    
    # Use patch as a decorator to mock the authorized_response function
    with patch('app.routes.auth_routes.github_authorized', return_value=mock_resp):
        # Use the Flask test client
        with client as c:
            with c.session_transaction() as sess:
                sess['github_token'] = None  # Set an initial value if needed

            # Call the mocked GitHub OAuth callback
            c.get('/auth/oauth/callback')

            # Assert that the session is updated correctly
            with c.session_transaction() as sess:
                assert 'github_token' in sess
                assert 'github_user' in sess
                assert sess['github_token'] == ('mock_access_token', '')
                assert sess['github_user']['login'] == 'mock_user'