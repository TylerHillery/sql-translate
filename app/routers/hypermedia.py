from typing import Annotated

import sqlglot
import sqlglot.errors
from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.models import CreateTranslation

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
        translation = sqlglot.transpile(
            sql=data.sql, read=data.from_dialect, write=data.to_dialect
        )
    except sqlglot.errors.ParseError as e:
        print(e)
        return
    except sqlglot.errors.UnsupportedError as e:
        print(e)
        return
    return templates.TemplateResponse(
        request, name="fragments/output-sql.html", context={"sql": translation[0]}
    )
