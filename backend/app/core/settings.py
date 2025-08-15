import os
from dotenv import load_dotenv
import stripe
from pydantic_settings import BaseSettings
from pydantic import ConfigDict


load_dotenv()


stripe_api_key = os.getenv("STRIPE_API_KEY")
if not stripe_api_key:
    raise RuntimeError("STRIPE_API_KEY is not set in .env")


stripe.api_key = stripe_api_key


class Settings(BaseSettings):
    MEDIA_ROOT: str = "media"
    MEDIA_URL: str = "/media"
    model_config = ConfigDict(env_file=".env", extra="ignore")

settings = Settings()