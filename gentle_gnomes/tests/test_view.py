import pytest


@pytest.mark.asyncio
async def test_index_response_200(client):
    res = await client.get('/')
    assert res.status_code == 200
