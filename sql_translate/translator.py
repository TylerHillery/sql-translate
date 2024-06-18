import itertools
import re
from dataclasses import dataclass
from typing import Optional

from sqlglot import errors, transpile

from sql_translate.utils import get_supported_sqlglot_dialects

SUPPORTED_DIALECTS = get_supported_sqlglot_dialects()


@dataclass
class SqlErrorDetails:
    description: Optional[str] = None
    line: Optional[int] = None
    col: Optional[int] = None
    start_context: Optional[str] = None
    highlight: Optional[str] = None
    end_context: Optional[str] = None
    into_expression: Optional[str] = None


@dataclass
class SqlTranslationResult:
    is_valid_sql: bool
    sql: str | SqlErrorDetails


def translate_sql(sql: str, from_dialect: str, to_dialect: str) -> SqlTranslationResult:
    """
    Translates an SQL query from one dialect to another while preserving the original
    whitespace and formatting. If the SQL query is invalid, the function returns an
    error message with details about the parsing error.

    Parameters:
    - sql (str): The input SQL query string to be translated.
    - from_dialect (str): The source SQL dialect.
    - to_dialect (str): The target SQL dialect.

    Returns:
    - SqlTranslationResult: A dataclass containing:
        - is_valid_sql (bool): True if the SQL query is valid and successfully translated,
                               False if there was a parsing error.
        - sql (str): The translated SQL query if valid, or an error message detailing the
                     parsing error if invalid.
    """
    from_dialect = from_dialect.strip().lower()
    to_dialect = to_dialect.strip().lower()

    if from_dialect not in SUPPORTED_DIALECTS:
        raise ValueError(
            f"Unsupported From Dialect: {from_dialect}. Supported dialects are: {SUPPORTED_DIALECTS}"
        )

    if to_dialect not in SUPPORTED_DIALECTS:
        raise ValueError(
            f"Unsupported To Dialect: {to_dialect}. Supported dialects are: {SUPPORTED_DIALECTS}"
        )

    sql_statements = re.split(r"(\s*;\s*)", sql)
    translated_sql = ""
    is_valid_sql = True
    i = 0
    while i < len(sql_statements) and is_valid_sql:
        sql_statement = sql_statements[i]
        whitespace = sql_statements[i + 1] if i + 1 < len(sql_statements) else ""
        try:
            translated_sql += (
                transpile(sql_statement, from_dialect, to_dialect)[0] + whitespace
            )
        except errors.ParseError as e:
            return SqlTranslationResult(False, SqlErrorDetails(**e.errors[0]))
        i += 2

    return SqlTranslationResult(is_valid_sql, restore_case(translated_sql, sql))


@dataclass
class CaseMapping:
    transpiled_token: str
    correct_case: str


def generate_case_mapping(transpiled: str, original: str) -> list[CaseMapping]:
    """
    Restores the case of the transpiled string based on the original string.

    Parameters:
    - transpiled (str): The transpiled string.
    - original (str): The original string.

    Returns:
    - list: List of CaseMapping dataclasses that has the transpiled token and it's
            corresponding correct case version of the transpiled version.

    The function works as follows:
    1. Tokenizes the original and transpiled SQL statements into words and keywords.
    2. Iterates through the tokens of both the original and transpiled SQL statements.
    3. If a direct case-insensitive match is found between tokens, it maps the transpiled token
       to the original token and appends it to case_mappings.
    4. If tokens do not match directly, it collects sequences of unmatched tokens from both
       the original and transpiled SQL. It does this by taking a copy of the transpiled_token_index
       and original_token_index and first compares the current transpiled_token to the remaining
       original_tokens. If it doesn't find a match for the remaining tokens, it then appends it
       to the no_match_transpiled_tokens list, iterates to the next transpiled_token, resets the
       original_token_index copy to the original_token_index, and runs until it either runs out of
       transpiled_tokens or matches a token in the original_tokens. Then it performs the same
       comparison but in the opposite direction to find the unmatched original tokens.
       The main logic is we don't want to add a token to a no-match list until
       it has done a full comparison of all the remaining tokens, which is why the loop runs twice:
       once to find the no-match transpiled tokens and once to find the no-match original tokens.
       This results in a worst-case scenario where every original token is compared to every
       transpiled token and vice versa, resulting in a Big O complexity of O(n^2). Optimization
       can be done in the future.
    5. Uses zip to align the unmatched tokens if the no-match transpiled tokens list is smaller
       or equal to the no-match original tokens. If the no-match transpiled tokens list is larger
       then is uses the zip_longest with the no-match original tokens last value as a fill value.
    6. Loops through the zip list, checking if the original token is upper case. If it is,
       appends the CaseMapping of the transpiled token to the upper() version of the
       transpiled token; otherwise, it maps it to the lower() version.
    """
    transpiled_tokens = [
        token
        for token in re.findall(r"\b\w+\b", transpiled)
        if token.isalpha() or "_" in token
    ]
    original_tokens = [
        token
        for token in re.findall(r"\b\w+\b", original)
        if token.isalpha() or "_" in token
    ]

    case_mappings = []
    transpiled_token_index, original_token_index = 0, 0

    while transpiled_token_index < len(
        transpiled_tokens
    ) and original_token_index < len(original_tokens):
        transpiled_token = transpiled_tokens[transpiled_token_index]
        original_token = original_tokens[original_token_index]

        if transpiled_token.upper() == original_token.upper():
            case_mappings.append(CaseMapping(transpiled_token, original_token))
            transpiled_token_index += 1
            original_token_index += 1
        else:
            no_match_transpiled_tokens, no_match_original_tokens = [], []

            i, j = transpiled_token_index, original_token_index
            while (
                i < len(transpiled_tokens)
                and transpiled_tokens[i].upper() != original_tokens[j].upper()
            ):
                j += 1
                if j >= len(original_tokens):
                    j = original_token_index
                    no_match_transpiled_tokens.append(transpiled_tokens[i])
                    i += 1

            i, j = transpiled_token_index, original_token_index
            while (
                j < len(original_tokens)
                and transpiled_tokens[i].upper() != original_tokens[j].upper()
            ):
                i += 1
                if i >= len(transpiled_tokens):
                    i = transpiled_token_index
                    no_match_original_tokens.append(original_tokens[j])
                    j += 1

            transpiled_token_index += len(no_match_transpiled_tokens)
            original_token_index += len(no_match_original_tokens)

            if len(no_match_transpiled_tokens) <= len(no_match_original_tokens):
                no_match_zipped = list(
                    zip(no_match_transpiled_tokens, no_match_original_tokens)
                )
            else:
                no_match_zipped = list(
                    itertools.zip_longest(
                        no_match_transpiled_tokens,
                        no_match_original_tokens,
                        fillvalue=no_match_original_tokens[-1],
                    )
                )

            for no_match_transpiled_token, no_match_original_token in no_match_zipped:
                if no_match_original_token.isupper():
                    case_mappings.append(
                        CaseMapping(
                            no_match_transpiled_token,
                            no_match_transpiled_token.upper(),
                        )
                    )
                else:
                    case_mappings.append(
                        CaseMapping(
                            no_match_transpiled_token,
                            no_match_transpiled_token.lower(),
                        )
                    )

    return case_mappings


def restore_case(transpiled: str, original: str) -> str:
    sql = ""

    for case_mapping in generate_case_mapping(transpiled, original):
        start = transpiled.find(case_mapping.transpiled_token)
        end = start + len(case_mapping.correct_case)

        sql += transpiled[:start] + case_mapping.correct_case

        transpiled = transpiled[end:]

    sql += transpiled

    return sql
