from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["data"]["docs"] == "/docs"


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["data"]["provider"] == "gemini"
    assert "X-Request-ID" in response.headers


def test_chat_validation_error():
    response = client.post(
        "/chat/",
        json={
            "message": "",
            "temperature": 5,
            "max_tokens": 10,
        },
    )

    assert response.status_code == 422

    body = response.json()

    assert body["success"] is False
    assert body["error_code"] == "VALIDATION_ERROR"
    assert body["request_id"] is not None