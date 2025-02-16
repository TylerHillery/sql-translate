from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import data, hypermedia

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(data.router)
app.include_router(hypermedia.router)
