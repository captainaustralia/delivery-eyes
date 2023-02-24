from fastapi.testclient import TestClient
from server import app

client = TestClient(app)


def test_get_pair_token():
    response = client.post(
        url="jwt/get_pair",
        json={
            "username": "string1",
            "password": "string"
        }
    )

    data = response.json()

    assert response.status_code == 200
    assert data["access"]
    assert data["refresh"]


def test_get_pair_token_wrong():
    response = client.post(
        url="jwt/get_pair",
        json={
            "username": "string",
            "password": "string"
        }
    )

    assert response.status_code == 403
