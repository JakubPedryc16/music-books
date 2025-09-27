
from pathlib import Path
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    CONFIG_DIR: Path = Path("data/tags/")
    TAGS_FILE: Path = Path("data/tags/tags.json")
    EMBEDDINGS_FILE: Path = Path("data/tags/tag_embeddings.npy")

    SPOTIPY_CLIENT_ID: str
    SPOTIPY_CLIENT_SECRET: str
    SPOTIPY_REDIRECT_URI: AnyHttpUrl
    SCOPE: str
    FRONTEND_URL: str
    JWT_SECRET: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
