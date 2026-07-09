import os
import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient

os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

from app.main import app
from app.database.init_db import init_db
from app.schemas.ai import AIResponse


client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def initialize_test_database():
    import asyncio
    asyncio.run(init_db())

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
    


def test_create_conversation():
    response = client.post("/conversations/")

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["data"]["conversation_id"]


def test_get_conversations():
    create_response = client.post("/conversations/")
    conversation_id = (
        create_response.json()["data"]["conversation_id"]
    )

    response = client.get("/conversations/")

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert {
        "conversation_id": conversation_id,
        "title": None,
    } in body["data"]["conversations"]


@patch(
    "app.services.ai_service.ai_service.chat",
    new_callable=AsyncMock,
)
@patch(
    "app.services.ai_service.ai_service.generate_conversation_title",
    new_callable=AsyncMock,
)
def test_send_conversation_message(
    mock_generate_conversation_title,
    mock_chat,
):
    mock_chat.return_value = AIResponse(
        content="Mocked assistant reply.",
        provider="gemini",
        model="gemini-2.5-flash",
        temperature=0.7,
        max_tokens=300,
        latency_ms=123,
    )
    mock_generate_conversation_title.return_value = "Greeting"

    create_response = client.post("/conversations/")
    conversation_id = (
        create_response.json()["data"]["conversation_id"]
    )

    response = client.post(
        f"/conversations/{conversation_id}/messages",
        json={
            "message": "Hello",
            "temperature": 0.7,
            "max_tokens": 300,
        },
    )

    assert response.status_code == 200

    messages = response.json()["data"]["messages"]

    assert len(messages) == 2
    assert messages[0]["role"] == "user"
    assert messages[1]["role"] == "assistant"


def test_get_unknown_conversation():
    response = client.get(
        "/conversations/not-a-real-id"
    )

    assert response.status_code == 404
    assert (
        response.json()["error_code"]
        == "CONVERSATION_NOT_FOUND"
    )
