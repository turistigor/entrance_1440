import pytest as pt

import httpx

from main import get_fastapi_app


@pt.fixture
async def api_client():
    fastapi_app = get_fastapi_app()
    async with httpx.AsyncClient(app=fastapi_app) as client:
        yield client
