import pytest
from httpx import ASGITransport, AsyncClient

from main import app


@pytest.fixture(autouse=True)
def set_test_env(monkeypatch):
    monkeypatch.setenv("INTERNAL_API_KEY", "test-key")
    monkeypatch.setenv("USE_FAKE_OPENAI", "true")


@pytest.mark.asyncio
async def test_chat_endpoint_success():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/chat",
            headers={"x-api-key": "test-key"},
            json={"user_input": "What is an RNN?"},
        )
        assert response.status_code == 200
        assert "mock transformer model" in response.json()["response"].lower()


@pytest.mark.asyncio
async def test_missing_api_key():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/chat", json={"user_input": "Hi"})
        # Now expect 401 Unauthorized when key is missing
        assert response.status_code == 403


@pytest.mark.asyncio
async def test_regression_chat_consistency():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {"user_input": "Explain Transformer architecture."}
        headers = {"x-api-key": "test-key"}

        r1 = await client.post("/chat", headers=headers, json=payload)
        r2 = await client.post("/chat", headers=headers, json=payload)

        assert r1.status_code == 200 and r2.status_code == 200
        assert r1.json()["response"] == r2.json()["response"]
