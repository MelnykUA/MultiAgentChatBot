import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_chat_endpoint_success(monkeypatch):
    monkeypatch.setenv("FAKE_OPENAI", "true")

    async with AsyncClient(base_url="http://test") as client:
        response = await client.post(
            "http://localhost:8000/chat",
            headers={"x-api-key": "staging-api-key-123"},
            json={"user_input": "What is an RNN?"}
        )
        assert response.status_code == 200
        assert "response" in response.json()
        assert response.json()["response"].startswith("def")
