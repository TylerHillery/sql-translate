import pytest

from app.translator import merge_sql_strings, parse_query_delimiters, restore_casing


def test_parse_query_delimeters():
    sql = "select * from table \n ;\t select * from table;\nselect * from table"
    expected_result = [" \n ;\t ", ";\n"]
    assert parse_query_delimiters(sql) == expected_result


def test_parse_query_delimeters_no_delimeter():
    sql = "select * from table \n"
    expected_result = []
    assert parse_query_delimiters(sql) == expected_result


def test_merge_sql_strings():
    queries = ["select * from table", "select * from table"]
    delimiters = [" ; "]
    expected_result = "select * from table ; select * from table"
    assert merge_sql_strings(queries, delimiters) == expected_result


def test_merge_sql_strings_no_delimiters():
    queries = ["select * from table"]
    delimiters = []
    expected_result = "select * from table"
    assert merge_sql_strings(queries, delimiters) == expected_result


def test_merge_sql_strings_no_queries():
    queries = []
    delimiters = []
    expected_result = ""
    assert merge_sql_strings(queries, delimiters) == expected_result


def test_merge_sql_strings_raises_value_error():
    queries = ["select * from table"]
    delimiters = [";", "; "]
    err_msg = (
        f"The number of delimiters ({len(delimiters)}) must be equal to or one less than the "
        f"number of queries ({len(queries)})."
    )

    with pytest.raises(ValueError) as excinfo:
        merge_sql_strings(queries, delimiters)

    assert err_msg in str(excinfo.value)


def test_restore_casing() -> None:
    original_sql = "select epoch_ms(1618088028295); SELECT EPOCH_MS(1618088028295)"
    transpiled_sql = "SELECT FROM_UNIXTIME(1618088028295 / POW(10, 3)); SELECT FROM_UNIXTIME(1618088028295 / POW(10, 3))"

    expected_result = "select from_unixtime(1618088028295 / pow(10, 3)); SELECT FROM_UNIXTIME(1618088028295 / POW(10, 3))"

    result = restore_casing(original_sql, transpiled_sql)

    assert result == expected_result
