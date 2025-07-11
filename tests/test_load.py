import asyncio

import pytest
from httpx import ASGITransport, AsyncClient

from main import app


@pytest.mark.asyncio
async def test_load_under_stress(monkeypatch):
    monkeypatch.setenv("USE_FAKE_OPENAI", "true")
    monkeypatch.setenv("INTERNAL_API_KEY", "staging-api-key-721")
    transport = ASGITransport(app=app)

    async def send_request():
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            res = await client.post(
                "/chat",
                headers={"x-api-key": "staging-api-key-721"},
                json={"user_input": "Define AI"},
            )
            assert res.status_code == 200
            assert "def" in res.json()["response"]

    # Simulate 10 parallel requests
    await asyncio.gather(*[send_request() for _ in range(10)])
