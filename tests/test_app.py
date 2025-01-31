import pytest
from app import app

@pytest.fixture
def client():
    return app.test_client()

def test_hello(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Hello from CI/CD Pipeline!" in response.data