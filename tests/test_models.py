import pytest

from app.models import CreateTranslation


def test_same_dialect_raises_error() -> None:
    with pytest.raises(ValueError) as excinfo:
        CreateTranslation(
            from_dialect="postgres", to_dialect="postgres", sql="select * from table"
        )
    assert "Dialects must diff" in str(excinfo.value)
