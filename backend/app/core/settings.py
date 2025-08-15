import os

from pydantic_settings import BaseSettings
from pydantic import ConfigDict

STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")

class Settings(BaseSettings):
    MEDIA_ROOT: str = "media"
    MEDIA_URL: str = "/media"
    model_config = ConfigDict(env_file=".env", extra="ignore")
settings = Settings()