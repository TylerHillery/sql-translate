from typing import Annotated

import sqlglot
import sqlglot.errors
from fastapi import APIRouter, Body, HTTPException, status

from app.config import settings
from app.models import CreateTranslation
from app.translator import merge_sql_strings, parse_query_delimiters, restore_casing

router = APIRouter(prefix=settings.API_V1_STR, tags=["Data API"])


@router.post("/translate")
async def create_translation(data: Annotated[CreateTranslation, Body()]) -> str:
    try:
        queries = sqlglot.transpile(
            sql=data.sql,
            read=data.from_dialect,
            write=data.to_dialect,
        )
    except sqlglot.errors.ParseError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=dict(error="ParseError", message=str(e), **e.errors[0]),
        )
    except sqlglot.errors.UnsupportedError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=dict(error="UnsupportedError", message=str(e)),
        )
    translation = merge_sql_strings(queries, parse_query_delimiters(data.sql))
    sql = restore_casing(data.sql, translation)
    return sql
