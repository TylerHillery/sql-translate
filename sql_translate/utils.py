from sqlglot import Dialect


def get_supported_sqlglot_dialects() -> list[str]:
    """
    Get a list of all supported SQL dialects by SQLGlot.

    Returns:
    - List[str]: A list of supported dialect names.
    """

    return sorted([dialect for dialect in Dialect.classes.keys() if dialect])
