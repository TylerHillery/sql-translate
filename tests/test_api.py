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
    expected_result = {"is_valid_sql": True, "sql": 'select * from "table"'}

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/translate", json=json_data)

    assert response.status_code == 200
    assert response.json() == expected_result


@pytest.mark.anyio
async def test_supported_dialects() -> None:
    expected_result = [
        "athena",
        "bigquery",
        "clickhouse",
        "databricks",
        "doris",
        "drill",
        "duckdb",
        "hive",
        "materialize",
        "mysql",
        "oracle",
        "postgres",
        "presto",
        "prql",
        "redshift",
        "risingwave",
        "snowflake",
        "spark",
        "spark2",
        "sqlite",
        "starrocks",
        "tableau",
        "teradata",
        "trino",
        "tsql",
    ]

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/dialects")

    assert response.status_code == 200
    assert response.json() == expected_result
