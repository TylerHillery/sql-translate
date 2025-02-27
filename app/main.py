from pathlib import Path

import modal
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.routers import data, hypermedia

web_app = FastAPI(title=settings.APP_NAME)
app = modal.App("sql_translate")


static_path = Path(__file__).parent.with_name("static").resolve()
static_remote_path = "/assets/static"
templates_path = Path(__file__).parent.with_name("templates").resolve()
templates_remote_path = "/assets/templates"
pyproject_toml_path = Path(__file__).parent.with_name("pyproject.toml").resolve()

image = (
    modal.Image.debian_slim(python_version="3.13")
    .pip_install_from_pyproject(str(pyproject_toml_path))
    .env({"ENVIRONMENT": "prod"})
    .add_local_dir(static_path, remote_path=static_remote_path)
    .add_local_dir(templates_path, remote_path=templates_remote_path)
)

static_files = (
    StaticFiles(directory=static_remote_path)
    if settings.ENVIRONMENT == "prod"
    else StaticFiles(directory=static_path)
)

web_app.mount("/static", static_files, name="static")

web_app.include_router(data.router)
web_app.include_router(hypermedia.router)


@app.function(image=image)
@modal.asgi_app()
def fastapi_app() -> FastAPI:
    return web_app
