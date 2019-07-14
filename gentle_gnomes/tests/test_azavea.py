import pytest


@pytest.mark.asyncio
async def test_request_data_exists(azavea):
    assert await azavea.get_indicators()
