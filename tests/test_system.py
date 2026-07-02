from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["success"] is True


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["success"] is True
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
    assert response.json()["error_code"] == "VALIDATION_ERROR"


@patch(
    "app.services.ai_service.ai_service.chat",
    new_callable=AsyncMock,
)
def test_chat_success(mock_chat):
    mock_chat.return_value = "This is a mocked AI response."

    response = client.post(
        "/chat/",
        json={
            "message": "Explain APIs",
            "temperature": 0.7,
            "max_tokens": 300,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["data"]["response"] == "This is a mocked AI response."
    assert body["request_id"] is not None

    mock_chat.assert_awaited_once()