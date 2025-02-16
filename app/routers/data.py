from typing import Annotated

import sqlglot
import sqlglot.errors
from fastapi import APIRouter, Body, HTTPException, status

from app.config import settings
from app.models import CreateTranslation

router = APIRouter(prefix=settings.API_V1_STR, tags=["Data API"])


@router.post("/translate")
async def create_translation(data: Annotated[CreateTranslation, Body()]) -> list[str]:
    # TODO:
    # need to handle when user sends multiple strings seperated by ;
    # SQLGlot doesn't preseve any white space before or after the ;
    try:
        # TODO: I want to parse all queries by ; so transpile only gets
        # one query. That way when we get errors we can assume [0] is okay
        translation = sqlglot.transpile(
            sql=data.sql,
            read=data.from_dialect,
            write=data.to_dialect,
            # TODO: maybe make this an optional body param
            unsupported_level=sqlglot.ErrorLevel.RAISE,
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
    return translation
