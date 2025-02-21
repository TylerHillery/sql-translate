from typing import Annotated

import sqlglot
import sqlglot.dialects
import sqlglot.dialects.dialect
from fastapi import APIRouter, Form, Header, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.models import CreateTranslation
from app.translator import merge_sql_strings, parse_query_delimiters, restore_casing

router = APIRouter(tags=["Hypermedia API"])


templates = Jinja2Templates(directory="templates")

SQLGLOT_FORMAT_SETTINGS = {
    "pretty": True,
    "leading_comma": False,
    "identify": False,
    "pad": 4,
    "indent": 4,
    "max_text_width": 80,
    "normalize": True,
    "normalize_functions": "lower",
}


@router.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    # TODO: add query param translation_id
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"dialects": sqlglot.dialects.DIALECTS},
    )


@router.get("/dialect-dropdown", response_class=HTMLResponse)
async def dialects_dopdown(
    request: Request,
    dialect: Annotated[str, Query()],
    hx_target: Annotated[str, Header()],
) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="fragments/dialect-dropdown.html",
        context={
            "dialects": sqlglot.dialects.DIALECTS,
            "selected_dialect": dialect,
            # TODO: I expect only from-dialect-dropdown and to-dialect-dropdown but should validate that
            "dialect_type": hx_target.split("-")[0],
        },
    )


@router.post("/translate", response_class=HTMLResponse)
async def create_translation(
    request: Request, data: Annotated[CreateTranslation, Form()]
) -> HTMLResponse:
    try:
        queries = sqlglot.transpile(
            sql=data.sql,
            read=data.from_dialect,
            write=data.to_dialect,
            **SQLGLOT_FORMAT_SETTINGS,  # type: ignore
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
    translation = restore_casing(data.sql, translation)

    return templates.TemplateResponse(
        request, name="fragments/output-sql.html", context={"sql": translation}
    )


@router.post("/format", response_class=HTMLResponse)
async def format(
    request: Request, data: Annotated[CreateTranslation, Form()]
) -> HTMLResponse:
    try:
        queries = sqlglot.transpile(
            sql=data.sql,
            read=data.from_dialect,
            write=data.from_dialect,
            **SQLGLOT_FORMAT_SETTINGS,  # type: ignore
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

    # TODO: add push url query_id
    translation = merge_sql_strings(queries, parse_query_delimiters(data.sql))
    translation = restore_casing(data.sql, translation)

    return templates.TemplateResponse(
        request, name="fragments/input-sql.html", context={"sql": translation}
    )
