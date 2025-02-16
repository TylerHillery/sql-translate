from sqlglot import Dialect


def get_supported_sqlglot_dialects() -> tuple[str, ...]:
    return tuple(sorted([dialect for dialect in Dialect.classes.keys() if dialect]))


SUPPORTED_DIALECTS = get_supported_sqlglot_dialects()
