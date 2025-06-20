import pytest

def test_root_redirect_to_home(client):
    """
    Test that the root URL '/' redirects to the '/home' route.
    """
    response = client.get('/')
    assert response.status_code == 302
    assert response.headers['Location'] == '/home'
