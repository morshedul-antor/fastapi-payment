from http.client import GATEWAY_TIMEOUT
from pydantic import AnyHttpUrl, BaseSettings, HttpUrl, validator
from typing import List, Optional, Union
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = os.environ.get("DATABASE_URL")
    SECRET_KEY: str = os.environ.get("SECRET_KEY")
    ALGORITHM: str = os.environ.get("ALGORITHM")
    STORE_ID: str = os.environ.get("STORE_ID")
    SIGNATURE_KEY: str = os.environ.get("SIGNATURE_KEY")
    GATEWAY_URL: str = os.environ.get("GATEWAY_URL")
    DETAILS_URL: str = os.environ.get("DETAILS_URL")

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        os.environ.get("URL_ONE"),
        os.environ.get("URL_TWO"),
    ]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = "FastAPI Payment"
    SENTRY_DSN: Optional[HttpUrl] = None

    class Config:
        case_sensitive = True


settings = Settings()
