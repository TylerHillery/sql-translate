from app.dialects import SUPPORTED_DIALECTS


def test_supported_dialects() -> None:
    assert SUPPORTED_DIALECTS == (
        "athena",
        "bigquery",
        "clickhouse",
        "databricks",
        "doris",
        "drill",
        "druid",
        "duckdb",
        "dune",
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
    )
