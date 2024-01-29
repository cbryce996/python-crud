import sys
import pytest
from app.main import create_app

# Fixture to create a test client for the Flask app
@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
    return app

# Fixture to provide a test client for each test function
@pytest.fixture
def client(app):
    return app.test_client()