from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    Secret_KEY: str = "w"
    DATABASE_URL: str = "sqlite:///app/database/global.db"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    MEDIA_ROOT: str = "media"
    MEDIA_URL: str = "/media"

    model_config = ConfigDict(env_file=".env", extra="ignore")

settings = Settings()
