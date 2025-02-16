from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["Hypermedia API"])


templates = Jinja2Templates(directory="templates")


@router.get("/")
async def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name="home.html")
