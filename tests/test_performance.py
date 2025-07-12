import asyncio

import pytest
from httpx import ASGITransport, AsyncClient

from main import app


@pytest.fixture(autouse=True)
def set_test_env(monkeypatch):
    monkeypatch.setenv("INTERNAL_API_KEY", "test-key")
    monkeypatch.setenv("USE_FAKE_OPENAI", "true")


@pytest.mark.asyncio
async def test_chat_performance_under_load():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        tasks = []
        for i in range(10):  # Adjust load here
            tasks.append(
                client.post(
                    "/chat",
                    headers={"x-api-key": "test-key"},
                    json={"user_input": f"What is tokenization? {i}"},
                )
            )
        responses = await asyncio.gather(*tasks)
        for res in responses:
            assert res.status_code == 200
