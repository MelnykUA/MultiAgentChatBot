import pytest
from httpx import ASGITransport, AsyncClient

from main import app


@pytest.mark.asyncio
async def test_regression_chat_endpoint_consistent_response(monkeypatch):
    # Use mocked OpenAI for consistent testing
    monkeypatch.setenv("FAKE_OPENAI", "true")
    monkeypatch.setenv("INTERNAL_API_KEY", "staging-api-key-721")
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {"user_input": "Explain Transformer architecture."}
        headers = {"x-api-key": "staging-api-key-721"}

        first_response = await client.post("/chat", json=payload, headers=headers)
        second_response = await client.post("/chat", json=payload, headers=headers)

        assert first_response.status_code == 200
        assert second_response.status_code == 200

        data1 = first_response.json()
        data2 = second_response.json()

        assert "response" in data1
        assert "response" in data2
        assert (
            data1["response"] == data2["response"]
        ), "Chat responses are inconsistent!"


@pytest.mark.asyncio
async def test_chat_endpoint_rejects_invalid_api_key():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {"user_input": "Test"}
        headers = {"x-api-key": "wrong-key"}
        response = await client.post("/chat", json=payload, headers=headers)
        assert response.status_code == 401
        assert response.json()["detail"] == "Unauthorized"
