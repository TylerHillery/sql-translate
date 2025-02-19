import re


def parse_query_delimiters(sql: str) -> list[str | None]:
    delimiters = re.findall(r"\s*;\s*", sql)
    return delimiters


def merge_sql_strings(queries: list[str], delimiters: list[str | None]) -> str:
    if not queries:
        return ""

    if not delimiters:
        return queries[0]

    if (n_queries := len(queries)) - 1 != (n_delimiters := len(delimiters)):
        raise ValueError(
            f"The number of delimiters ({n_delimiters}) must be one less than the "
            f"number of queries ({n_queries})."
        )

    return "".join(
        [f"{query}{delimiter}" for query, delimiter in zip(queries, delimiters)]
        + [queries[-1]]
    )
