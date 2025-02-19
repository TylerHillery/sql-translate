from typing import Any, Self

from pydantic import BaseModel, field_validator, model_validator

from app.custom_types import SupportedDialects


class CreateTranslation(BaseModel):
    from_dialect: SupportedDialects
    to_dialect: SupportedDialects | None = None
    sql: str

    @field_validator("from_dialect", "to_dialect", mode="before")
    @classmethod
    def lower(cls, value: str | Any) -> str | Any:
        if isinstance(value, str):
            return value.lower()
        return value

    @model_validator(mode="after")
    def dialects_must_differ(self) -> Self:
        if self.to_dialect is None:
            self.to_dialect = self.from_dialect
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
