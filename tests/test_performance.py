# tests/test_performance.py

import asyncio

import pytest
from httpx import ASGITransport, AsyncClient

from main import app


@pytest.mark.asyncio
async def test_chat_performance_under_load():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        tasks = []
        for i in range(10):  # Adjust for load
            tasks.append(
                client.post(
                    "/chat",
                    headers={"x-api-key": "staging-api-key-721"},
                    json={"user_input": f"What is tokenization? {i}"},
                )
            )
        responses = await asyncio.gather(*tasks)
        for res in responses:
            assert res.status_code == 200
