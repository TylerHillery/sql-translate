from fastapi import FastAPI

from sql_translate.models import SqlTranslationRequest, SqlTranslationResponse
from sql_translate.translator import translate_sql

web_app = FastAPI()


@web_app.post("/translate", response_model=SqlTranslationResponse)
async def translate(request: SqlTranslationRequest) -> SqlTranslationResponse:
    return translate_sql(
        sql=request.sql,
        from_dialect=request.from_dialect,
        to_dialect=request.to_dialect,
        options=request.options,
    )
