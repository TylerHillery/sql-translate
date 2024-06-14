import importlib
from pathlib import Path


def get_supported_sqlglot_dialects() -> list[str]:
    """
    Get a list of all supported SQL dialects by SQLGlot.

    Returns:
    - List[str]: A list of supported dialect names.
    """
    sqlglot_dialects_module = importlib.import_module("sqlglot.dialects")

    if (module_file := sqlglot_dialects_module.__file__) is None:
        raise ValueError(
            "Could not determine the file path of the sqlglot.dialects module."
        )

    dialects = [
        file.with_suffix("").name
        for file in sorted(Path(module_file).parent.glob("*.py"))
        if file.name != "__init__.py"
    ]

    return dialects
