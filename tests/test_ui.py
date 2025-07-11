# tests/test_ui(api).py

import pytest
from httpx import ASGITransport, AsyncClient

from main import app  # Ensure this path matches your FastAPI app


@pytest.mark.asyncio
async def test_chat_endpoint_success(monkeypatch):
    monkeypatch.setenv("USE_FAKE_OPENAI", "true")
    monkeypatch.setenv("INTERNAL_API_KEY", "staging-api-key-721")
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/chat",
            headers={"x-api-key": "staging-api-key-721"},
            json={"user_input": "What is an RNN?"},
        )
        assert response.status_code == 200
        assert "mock transformer model" in response.json()["assistant_response"].lower()
