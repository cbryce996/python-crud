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

@patch.object(github, 'get', side_effect=[MagicMock(data=mock_user_data), MagicMock(data=mock_repo_data)])
@patch.object(github, 'authorized_response', return_value={'access_token': 'fake_token'})
def test_github_authorized(patch_authorized_response, patch_get, client):
    response = client.get('/auth/oauth/callback')
    print(response)

    print(f"Class being patched: {github.__class__}")
    print(f"Method being patched: {github.authorized_response}")

    # Check if user data is NOT stored in the session
    with client.session_transaction() as sess:
        assert 'github_token' in sess
        assert 'github_user' in sess

    assert response.status_code == 302  # Ensure it redirects after successful authentication