from pydantic import BaseModel, model_validator
from typing_extensions import Self

from app.custom_types import SupportedDialects


class CreateTranslation(BaseModel):
    from_dialect: SupportedDialects
    to_dialect: SupportedDialects
    sql: str

    @model_validator(mode="after")
    def dialects_must_differ(self) -> Self:
        if self.from_dialect == self.to_dialect:
            raise ValueError("Dialects must differ")
        return self

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
