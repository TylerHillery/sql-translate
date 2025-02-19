from app.models import CreateTranslation


def test_create_translation_none_to_dialect():
    data = CreateTranslation.model_validate(
        {
            "from_dialect": "mysql",
            "sql": "select date_format(now(), '%Y-%m-%d') as formatted_date;",
        }
    )
    assert data.to_dialect == "mysql"


def test_create_translation_lowercase_validator():
    data = CreateTranslation.model_validate(
        {
            "from_dialect": "MySQL",
            "to_dialect": "Postgres",
            "sql": "select date_format(now(), '%Y-%m-%d') as formatted_date;",
        }
    )
    assert data.from_dialect == "mysql"
    assert data.to_dialect == "postgres"
