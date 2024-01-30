from flask import url_for
from urllib.parse import urlparse
from pytest import fixture
from unittest.mock import MagicMock, patch
from app.views.auth import github
from main import create_app, register_routes
from .fixtures import mock_user_data, mock_repo_data

@fixture
def app():
    """
    Fixture to generate an app context.

    Creates and configures the app, then registers routes.
    """
    app = create_app()
    register_routes(app)
    return app

@patch.object(github, 'get', side_effect=[MagicMock(data=mock_user_data), MagicMock(data=mock_repo_data)])
@patch.object(github, 'authorized_response', return_value={'access_token': 'fake_token'})
def test_github_authorized(patch_authorized_response, patch_get, client):
    """
    Test the GitHub OAuth callback.

    Ensures that session variables are set correctly and the user is redirected to the profile page.
    """
    response = client.get('/auth/oauth/callback')

    with client.session_transaction() as sess:
        assert 'github_token' in sess
        assert 'github_user' in sess

    assert response.status_code == 302

    with client.application.test_request_context():
        expected_redirect_url = url_for('user_views.profile', _external=True)
        expected_path = urlparse(expected_redirect_url).path
        assert expected_path in urlparse(response.location).path

def test_logout_route(client):
    """
    Test the logout route.

    Ensures that session variables are cleared and the user is redirected to the login page.
    """
    with client.session_transaction() as session:
        session['github_user'] = {'some_key': 'some_value'}
        session['github_token'] = 'fake_token'

    response = client.get('/auth/logout')

    with client.session_transaction() as session:
        assert 'github_user' not in session
        assert 'github_token' not in session

    assert response.status_code == 302

    with client.application.test_request_context():
        expected_redirect_url = url_for('auth_views.login', _external=True)
        expected_path = urlparse(expected_redirect_url).path
        assert expected_path in urlparse(response.location).path

def test_profile_route_without_token(client):
    """
    Test the profile route without session variables.

    Ensures that the user is redirected to the login page.
    """
    response = client.get('/user/profile')

    assert response.status_code == 302

    with client.application.test_request_context():
        expected_redirect_url = url_for('auth_views.login', _external=True)
        expected_path = urlparse(expected_redirect_url).path
        assert expected_path in urlparse(response.location).path

def test_edit_route_without_token(client):
    """
    Test the edit route without session variables.

    Ensures that the user is redirected to the login page.
    """
    response = client.get('/user/edit')

    assert response.status_code == 302

    with client.application.test_request_context():
        expected_redirect_url = url_for('auth_views.login', _external=True)
        expected_path = urlparse(expected_redirect_url).path
        assert expected_path in urlparse(response.location).path
