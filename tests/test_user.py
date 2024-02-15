from unittest.mock import Mock, patch
from urllib.parse import urlparse

from flask import url_for
from pytest import fixture

from main import create_app, register_routes

from .fixtures import mock_processed_user_data


@fixture
def app():
    """
    Fixture to generate an app context.

    Creates and configures the app, then registers routes.
    """
    app = create_app()
    register_routes(app)
    return app


@fixture
def mocker():
    """
    Mock fixture to generate

    Creates and configures the app, then registers routes.
    """
    return Mock()


@patch("app.views.user.update_github_user", return_value=True)
def test_edit_route_successful_update(mock_update_github_user, client):
    """
    Test the edit route with a successful user data update.

    Ensures that the form submission leads to a successful update of GitHub user data.
    """
    with patch("app.views.user.EditForm") as mock_form:
        mock_form_instance = mock_form.return_value
        mock_form_instance.validate_on_submit.return_value = True

        mock_form_instance.name.data = "John Doe"
        mock_form_instance.location.data = "Dummy City, Dummy Country"
        mock_form_instance.bio.data = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla quis tristique elit."

        with client.session_transaction() as session:
            session["github_user"] = mock_processed_user_data
            session["github_token"] = ("fake_token", "")

        response = client.post("/user/edit")

        assert response.status_code == 302

        with client.application.test_request_context():
            expected_redirect_url = url_for("user_views.profile", _external=True)
            expected_path = urlparse(expected_redirect_url).path
            assert expected_path in urlparse(response.location).path


@patch("app.views.user.update_github_user", return_value=False)
def test_edit_route_failed_update(mock_update_github_user, client):
    """
    Test the edit route with a successful user data update.

    Ensures that the form submission leads to a successful update of GitHub user data.
    """
    with patch("app.views.user.EditForm") as mock_form:
        mock_form_instance = mock_form.return_value
        mock_form_instance.validate_on_submit.return_value = True

        mock_form_instance.name.data = "John Doe"
        mock_form_instance.location.data = "Dummy City, Dummy Country"
        mock_form_instance.bio.data = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla quis tristique elit."

        with client.session_transaction() as session:
            session["github_user"] = mock_processed_user_data
            session["github_token"] = ("fake_token", "")

        response = client.post("/user/edit")

        # No redirect results in no update
        assert response.status_code == 200
