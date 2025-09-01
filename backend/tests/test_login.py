import os
import sys
import pytest

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, 'venv', 'lib', 'python3.9', 'site-packages'))
sys.path.insert(0, BASE_DIR)
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_login_missing_json(client):
    response = client.post('/auth/login')
    assert response.status_code == 400
    assert response.get_json()['erro'] == 'corpo JSON ausente ou inválido'


def test_login_invalid_json(client):
    response = client.post('/auth/login', data='invalid', content_type='application/json')
    assert response.status_code == 400
    assert response.get_json()['erro'] == 'corpo JSON ausente ou inválido'

