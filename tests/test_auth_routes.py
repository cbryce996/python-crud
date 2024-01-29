from flask import url_for
from urllib.parse import urlparse
from pytest import fixture
from unittest.mock import MagicMock, patch
from app.routes.auth_routes import github
from main import create_app, register_routes
from .fixtures import mock_user_data, mock_repo_data

@fixture
def app():
    app = create_app()
    register_routes(app)
    return app

# Tests OAuth requests and checks if session variables are set and redirect is correct

@patch.object(github, 'get', side_effect=[MagicMock(data=mock_user_data), MagicMock(data=mock_repo_data)])
@patch.object(github, 'authorized_response', return_value={'access_token': 'fake_token'})
def test_github_authorized(patch_authorized_response, patch_get, client):
    response = client.get('/auth/oauth/callback')

    with client.session_transaction() as sess:
        assert 'github_token' in sess
        assert 'github_user' in sess

    assert response.status_code == 302

    with client.application.test_request_context():
        # Check that the redirect URL contains the correct endpoint
        expected_redirect_url = url_for('user_routes.profile', _external=True)
        expected_path = urlparse(expected_redirect_url).path
        assert expected_path in urlparse(response.location).path

# Tests logout to ensure session variables are destroyed

def test_logout_route(client):
    with client.session_transaction() as session:
        session['github_user'] = {'some_key': 'some_value'}
        session['github_token'] = 'fake_token'

    response = client.get('/auth/logout')

    with client.session_transaction() as session:
        assert 'github_user' not in session
        assert 'github_token' not in session

    assert response.status_code == 302

    with client.application.test_request_context():
        # Check that the redirect URL contains the correct endpoint
        expected_redirect_url = url_for('auth_routes.login', _external=True)
        expected_path = urlparse(expected_redirect_url).path
        assert expected_path in urlparse(response.location).path

# Tests if profile page redirects to login without session variables

def test_profile_route_without_token(client):
    response = client.get('/user/profile')
    
    assert response.status_code == 302

    with client.application.test_request_context():
        # Check that the redirect URL contains the correct endpoint
        expected_redirect_url = url_for('auth_routes.login', _external=True)
        expected_path = urlparse(expected_redirect_url).path
        assert expected_path in urlparse(response.location).path

# Tests if edit page redirects to login without session variables

def test_edit_route_without_token(client):
    response = client.get('/user/edit')
    
    assert response.status_code == 302

    with client.application.test_request_context():
        # Check that the redirect URL contains the correct endpoint
        expected_redirect_url = url_for('auth_routes.login', _external=True)
        expected_path = urlparse(expected_redirect_url).path
        assert expected_path in urlparse(response.location).path