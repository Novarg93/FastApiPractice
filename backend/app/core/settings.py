from pydantic_settings import BaseSettings
from pydantic import ConfigDict
class Settings(BaseSettings):
    MEDIA_ROOT: str = "media"
    MEDIA_URL: str = "/media"
    # ... остальные поля ...
    model_config = ConfigDict(env_file=".env", extra="ignore")
settings = Settings()