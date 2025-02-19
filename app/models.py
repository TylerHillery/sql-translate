from pydantic import BaseModel

from app.custom_types import SupportedDialects


class CreateTranslation(BaseModel):
    from_dialect: SupportedDialects
    to_dialect: SupportedDialects
    sql: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "from_dialect": "mysql",
                    "to_dialect": "postgres",
                    "sql": "select date_format(now(), '%Y-%m-%d') as formatted_date;",
                }
            ]
        }
    }
