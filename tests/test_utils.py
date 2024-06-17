from unittest.mock import MagicMock, patch

import pytest

from sql_translate.utils import get_supported_sqlglot_dialects


def test_get_supported_sqlglot_dialects() -> None:
    expected_result = [
        "athena",
        "bigquery",
        "clickhouse",
        "databricks",
        "dialect",
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


def test_get_supported_sqlglot_dialects_raises_import_error() -> None:
    mock_module = MagicMock()
    mock_module.__file__ = None

    with patch("importlib.import_module", return_value=mock_module):
        with pytest.raises(
            ImportError,
            match="Could not determine the file path of the sqlglot.dialects module.",
        ):
            get_supported_sqlglot_dialects()
