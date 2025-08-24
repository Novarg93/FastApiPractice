# app/core/settings.py
import stripe
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    STRIPE_API_KEY: str

    MEDIA_ROOT: str = "media"
    MEDIA_URL: str = "/media"

    model_config = ConfigDict(env_file=".env", extra="ignore")

settings = Settings()

stripe.api_key = settings.STRIPE_API_KEY

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES