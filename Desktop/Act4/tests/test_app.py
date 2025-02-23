import pytest
from src.app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_hello_world(client):
    """Test the root endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    assert response.data == b'Hello, World!'
