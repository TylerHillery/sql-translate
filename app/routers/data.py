from typing import Annotated

from fastapi import APIRouter, Body
from sqlglot import transpile

from app.dependencies import get_settings
from app.models import CreateTranslation

settings = get_settings()

router = APIRouter(prefix=settings.APP_VI_STR, tags=["Data API"])


@router.post("/translate")
async def create_translation(data: Annotated[CreateTranslation, Body()]) -> list[str]:
    translation = transpile(sql=data.sql, read=data.from_dialect, write=data.to_dialect)
    return translation
