from pathlib import Path

import modal
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.routers import data, hypermedia

web_app = FastAPI(title=settings.APP_NAME)
app = modal.App(name=settings.APP_NAME)


static_path = Path(__file__).parent.with_name("static").resolve()
templates_path = Path(__file__).parent.with_name("templates").resolve()
pyproject_toml_path = Path(__file__).parent.with_name("pyproject.toml").resolve()

image = (
    modal.Image.debian_slim(python_version="3.13")
    .pip_install_from_pyproject(str(pyproject_toml_path))
    .env({"ENVIRONMENT": "prod"})
    .add_local_dir(static_path, remote_path="/static")
    .add_local_dir(templates_path, remote_path="/templates")
)

web_app.mount("/static", StaticFiles(directory=static_path), name="static")

web_app.include_router(data.router)
web_app.include_router(hypermedia.router)


@app.function(image=image)
@modal.asgi_app()
def fastapi_app() -> FastAPI:
    return web_app
