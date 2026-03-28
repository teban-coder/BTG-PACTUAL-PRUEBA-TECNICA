from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_subscribe():
    # Login primero
    login = client.post("/login?user_id=1&password=1234")
    assert login.status_code == 200

    token = login.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = client.post("/subscribe/1/1", headers=headers)

    assert response.status_code == 200
    assert response.json()["mensaje"] == "Suscripción exitosa"