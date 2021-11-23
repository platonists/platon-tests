import asyncio
import pytest
import time


@pytest.mark.asyncio
async def test_a():
    time.sleep(2)
    await asyncio.sleep(5)


@pytest.mark.asyncio
async def test_b():
    await asyncio.sleep(3)


