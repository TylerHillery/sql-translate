from pathlib import Path

from fastapi import FastAPI
from modal import App, Image, Mount, asgi_app

ASSETS_PATH = Path(__file__).parent / "frontend" / "dist"

app = App("sql-translator")
app.image = Image.debian_slim().pip_install_from_requirements("requirements.txt")


@app.function(mounts=[Mount.from_local_dir(ASSETS_PATH, remote_path="/assets")])
@asgi_app()
def fastapi_app() -> FastAPI:
    import fastapi.staticfiles

    from sql_translate.api import web_app

    web_app.mount("/", fastapi.staticfiles.StaticFiles(directory="/assets", html=True))

    return web_app
