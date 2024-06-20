import pytest
from httpx import AsyncClient, ASGITransport

from sql_translate.api import web_app

transport = ASGITransport(app=web_app)


@pytest.mark.anyio
async def test_translate() -> None:
    json_data = {
        "sql": "select * from table",
        "from_dialect": "postgres",
        "to_dialect": "duckdb",
        "options": {"identify": False},
    }
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/translate", json=json_data)
    assert response.status_code == 200
    result = response.json()
    expected_result = {"is_valid_sql": True, "sql": 'select * from "table"'}
    assert result == expected_result
