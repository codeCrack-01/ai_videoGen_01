import pytest
from app import app

@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as client:
        # Flask sessions require a SECRET_KEY to be set, which you've done in app.py.
        # However, for testing session data, you often need to enable session transactions.
        # This allows you to inspect and modify session data within tests.
        with app.app_context():
            # Any setup that needs the app context (like database connections if you had them)
            # would go here. For now, it's good practice.
            pass
        yield client # This yields the client for use in tests

@pytest.fixture
def app_context():
    """Provides an application context for testing."""
    with app.app_context():
        yield
