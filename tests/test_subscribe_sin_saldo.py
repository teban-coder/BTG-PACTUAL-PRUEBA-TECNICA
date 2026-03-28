from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_subscribe_sin_saldo():
    # Login
    login = client.post("/login?user_id=1&password=1234")
    assert login.status_code == 200

    token = login.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Intentar varias veces para agotar saldo
    for _ in range(10):
        client.post("/subscribe/1/4", headers=headers)

    response = client.post("/subscribe/1/4", headers=headers)

    assert response.status_code == 400