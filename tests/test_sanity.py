import pytest
from httpx import ASGITransport, AsyncClient

from main import app


@pytest.mark.asyncio
async def test_root_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/")
        assert res.status_code == 200
        assert res.json() == {"message": "Multi-Agent Chatbot API is running."}


@pytest.mark.asyncio
async def test_missing_api_key(monkeypatch):
    # Set expected API key in env
    monkeypatch.setenv("INTERNAL_API_KEY", "test-key")

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.post("/chat", json={"user_input": "Hello?"})
        assert res.status_code == 401
        assert res.json()["detail"] == "Unauthorized"
