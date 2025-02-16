from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "SQL Translate"
    APP_VI_STR: str = "/api/vi"
    ENVIRONMENT: Literal["dev", "staging", "prod"] = "dev"
