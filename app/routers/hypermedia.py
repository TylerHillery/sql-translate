from typing import Annotated

import sqlglot
import sqlglot.errors
from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.models import CreateTranslation
from app.translator import merge_sql_strings, parse_query_delimiters

router = APIRouter(tags=["Hypermedia API"])


templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name="home.html")


@router.post("/translate", response_class=HTMLResponse)
async def create_translation(
    request: Request, data: Annotated[CreateTranslation, Form()]
) -> HTMLResponse:
    try:
        queries = sqlglot.transpile(
            sql=data.sql, read=data.from_dialect, write=data.to_dialect
        )
    except sqlglot.errors.ParseError as e:
        # TODO: figure out how to format error message
        return templates.TemplateResponse(
            request, name="fragments/output-sql.html", context={"sql": str(e)}
        )
    except sqlglot.errors.UnsupportedError as e:
        # TODO: figure out how to format error message
        return templates.TemplateResponse(
            request, name="fragments/output-sql.html", context={"sql": str(e)}
        )

    translation = merge_sql_strings(queries, parse_query_delimiters(data.sql))

    return templates.TemplateResponse(
        request, name="fragments/output-sql.html", context={"sql": translation}
    )
