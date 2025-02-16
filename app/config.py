from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "SQL Translate"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: Literal["dev", "staging", "prod"] = "dev"


settings = Settings()
