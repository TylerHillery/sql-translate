from typing import List

from fastapi import FastAPI

from sql_translate.models import SqlTranslationRequest, SqlTranslationResponse
from sql_translate.translator import translate_sql
from sql_translate.utils import get_supported_sqlglot_dialects

web_app = FastAPI()


@web_app.post("/translate", response_model=SqlTranslationResponse)
async def translate(request: SqlTranslationRequest) -> SqlTranslationResponse:
    return translate_sql(
        sql=request.sql,
        from_dialect=request.from_dialect,
        to_dialect=request.to_dialect,
        options=request.options,
    )


@web_app.get("/dialects", response_model=List[str])
async def supported_dialects() -> List[str]:
    return get_supported_sqlglot_dialects()
