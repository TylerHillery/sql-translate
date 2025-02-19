import pytest

from app.translator import merge_sql_strings, parse_query_delimiters


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
        f"The number of delimiters ({len(delimiters)}) must be one less than the "
        f"number of queries ({len(queries)})."
    )

    with pytest.raises(ValueError) as excinfo:
        merge_sql_strings(queries, delimiters)

    assert err_msg in str(excinfo.value)
