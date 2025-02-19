import re
from typing import Callable


def parse_query_delimiters(sql: str) -> list[str | None]:
    delimiters = re.findall(r"\s*;\s*", sql)
    return delimiters


def merge_sql_strings(queries: list[str], delimiters: list[str | None]) -> str:
    if not queries:
        return ""

    if not delimiters:
        return queries[0]

    n_queries = len(queries)
    n_delimiters = len(delimiters)
    diff = n_queries - n_delimiters

    if n_delimiters != n_queries and n_delimiters != (n_queries - 1):
        raise ValueError(
            f"The number of delimiters ({n_delimiters}) must be equal to or one less than the "
            f"number of queries ({n_queries})."
        )

    result = "".join(
        [f"{query}{delimiter}" for query, delimiter in zip(queries, delimiters)]
    )

    if diff == 1:
        result += queries[-1]

    return result


def get_casing(words: list[str]) -> Callable[[str], str]:
    first_alpha = next((char for char in "".join(words) if char.isalpha()), "a")
    return str.upper if first_alpha.isupper() else str.lower


def restore_casing(original: str, transpiled: str) -> str:
    """
    SQLGlot doesn't preserve the original casing of the original sql string.
    This function does a 'best effort' job of trying to restore the orignal casing.

    This is done by comparing each 'word' from the original sql string to the
    transpiled sql string. It looks for exact matches based on a case insensitive
    comparison.

    We then figure out "implied" matches based on any words it skips.

    Once the how the range of original words maps to the range of transpiled words
    we apply the casing of the original word based on the first letter.
    """
    original_words = re.split(r"(\s+)", original)
    transpiled_words_lower = re.split(r"(\s+)", transpiled.lower())
    original_mapping = []
    transpiled_mapping = []
    last_original_match_idx = 0
    last_transpiled_match_idx = 0
    for original_idx, original_word in enumerate(original_words):
        if original_word.isspace():
            continue

        original_word_lower = original_word.lower()
        transpiled_words_subset = transpiled_words_lower[last_transpiled_match_idx:]

        if original_word_lower in transpiled_words_subset:
            transpiled_index = transpiled_words_subset.index(original_word_lower)
            transpiled_index += last_transpiled_match_idx

            if (original_idx - last_original_match_idx) > 0:
                original_mapping.append(
                    get_casing(original_words[last_original_match_idx:original_idx])
                )
            original_mapping.append(
                get_casing(original_words[original_idx : (original_idx + 1)])
            )
            last_original_match_idx = original_idx + 1

            if (transpiled_index - last_transpiled_match_idx) > 0:
                transpiled_mapping.append((last_transpiled_match_idx, transpiled_index))
            transpiled_mapping.append((transpiled_index, transpiled_index + 1))
            last_transpiled_match_idx = transpiled_index + 1

    if last_original_match_idx < len(original_words):
        original_mapping.append(
            get_casing(original_words[last_original_match_idx : len(original_words)])
        )

    if last_transpiled_match_idx < len(transpiled_words_lower):
        transpiled_mapping.append(
            (last_transpiled_match_idx, len(transpiled_words_lower))
        )

    result = ""
    for case_func, (start_idx, end_idx) in zip(original_mapping, transpiled_mapping):
        for word in transpiled_words_lower[start_idx:end_idx]:
            result += case_func(word)

    return result


if __name__ == "__main__":
    input = "SELECT FROM_UNIXTIME(1618088028295 / POW(10, 3)); select from_unixtime(1618088028295 / POW(10, 3))"
    output = "SELECT EPOCH_MS(1618088028295); SELECT EPOCH_MS(1618088028295)"
    print("Input: ", input)
    print("Transpiled: ", output)
    print("Result: ", restore_casing(input, output))
