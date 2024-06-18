import pytest

from sql_translate.translator import (
    CaseMapping,
    SqlErrorDetails,
    SqlTranslationResult,
    generate_case_mapping,
    translate_sql,
    restore_case,
)


def test_invalid_from_dialect() -> None:
    sql = "SELECT 1;"
    from_dialect = "invalid_dialect"
    to_dialect = "hive"

    with pytest.raises(ValueError, match=r"Unsupported From Dialect: invalid_dialect"):
        translate_sql(sql, from_dialect, to_dialect)


def test_invalid_to_dialect() -> None:
    sql = "SELECT 1;"
    from_dialect = "duckdb"
    to_dialect = "invalid_dialect"

    with pytest.raises(ValueError, match=r"Unsupported To Dialect: invalid_dialect"):
        translate_sql(sql, from_dialect, to_dialect)


def test_multiple_sql_statements_with_ending_semicolon() -> None:
    sql = "SELECT EPOCH_MS(1618088028295); select EPOCH_MS(1618088028295);"
    from_dialect = "duckdb"
    to_dialect = "hive"

    expected_result = "SELECT FROM_UNIXTIME(1618088028295 / POW(10, 3)); select FROM_UNIXTIME(1618088028295 / POW(10, 3));"
    result = translate_sql(sql, from_dialect, to_dialect)

    assert result == SqlTranslationResult(is_valid_sql=True, sql=expected_result)


def test_multiple_sql_statements_without_ending_semicolon() -> None:
    sql = "SELECT epoch_ms(1618088028295); SELECT EPOCH_MS(1618088028295)"
    from_dialect = "duckdb"
    to_dialect = "hive"

    expected_result = "SELECT from_unixtime(1618088028295 / pow(10, 3)); SELECT FROM_UNIXTIME(1618088028295 / POW(10, 3))"
    result = translate_sql(sql, from_dialect, to_dialect)

    assert result == SqlTranslationResult(is_valid_sql=True, sql=expected_result)


def test_sql_with_various_whitespace() -> None:
    sql = "select EPOCH_MS(1618088028295)\n;\n\tselect EPOCH_MS(1618088028295)"
    from_dialect = "duckdb"
    to_dialect = "hive"

    expected_result = "select FROM_UNIXTIME(1618088028295 / POW(10, 3))\n;\n\tselect FROM_UNIXTIME(1618088028295 / POW(10, 3))"
    result = translate_sql(sql, from_dialect, to_dialect)

    assert result == SqlTranslationResult(is_valid_sql=True, sql=expected_result)


def test_invalid_sql_with_error() -> None:
    sql = "SELECT * FROM FROM;"
    from_dialect = "duckdb"
    to_dialect = "hive"

    expected_result = SqlErrorDetails(
        description="Expected table name but got None",
        line=1,
        col=18,
        start_context="SELECT * FROM ",
        highlight="FROM",
        end_context="",
        into_expression=None,
    )
    result = translate_sql(sql, from_dialect, to_dialect)

    assert result.is_valid_sql is False
    assert result.sql == expected_result


def test_generate_case_mapping() -> None:
    transpiled_sql = "SELECT FROM_UNIXTIME(1618088028295 / POW(10, 3))\n;\n\tSELECT FROM_UNIXTIME(1618088028295 / POW(10, 3))"
    original_sql = "select epoch_ms(1618088028295)\n;\n\tSELECT EPOCH_MS(1618088028295)"

    expected_result = [
        CaseMapping(transpiled_token="SELECT", correct_case="select"),
        CaseMapping(transpiled_token="FROM_UNIXTIME", correct_case="from_unixtime"),
        CaseMapping(transpiled_token="POW", correct_case="pow"),
        CaseMapping(transpiled_token="SELECT", correct_case="SELECT"),
        CaseMapping(transpiled_token="FROM_UNIXTIME", correct_case="FROM_UNIXTIME"),
        CaseMapping(transpiled_token="POW", correct_case="POW"),
    ]

    result = generate_case_mapping(transpiled_sql, original_sql)

    assert result == expected_result


def test_generate_case_mapping_reverse() -> None:
    transpiled_sql = (
        "SELECT EPOCH_MS(1618088028295)\n;\n\tSELECT EPOCH_MS(1618088028295)"
    )
    original_sql = "select from_unixtime(1618088028295 / pow(10, 3))\n;\n\tSELECT FROM_UNIXTIME(1618088028295 / POW(10, 3))"

    expected_result = [
        CaseMapping(transpiled_token="SELECT", correct_case="select"),
        CaseMapping(transpiled_token="EPOCH_MS", correct_case="epoch_ms"),
        CaseMapping(transpiled_token="SELECT", correct_case="SELECT"),
        CaseMapping(transpiled_token="EPOCH_MS", correct_case="EPOCH_MS"),
    ]

    result = generate_case_mapping(transpiled_sql, original_sql)

    assert result == expected_result


def test_restore_case() -> None:
    transpiled_sql = "SELECT FROM_UNIXTIME(1618088028295 / POW(10, 3)); SELECT FROM_UNIXTIME(1618088028295 / POW(10, 3))"
    original_sql = "select epoch_ms(1618088028295); SELECT EPOCH_MS(1618088028295)"

    expected_result = "select from_unixtime(1618088028295 / pow(10, 3)); SELECT FROM_UNIXTIME(1618088028295 / POW(10, 3))"

    result = restore_case(transpiled_sql, original_sql)

    assert result == expected_result
