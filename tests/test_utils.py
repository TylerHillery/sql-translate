from sql_translate.utils import get_supported_sqlglot_dialects


def test_get_supported_sqlglot_dialects() -> None:
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

    result = get_supported_sqlglot_dialects()

    assert result == expected_result
