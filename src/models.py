# src/models.py
import os
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings

# Settings class
class Settings(BaseSettings):
    LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL")  # Default to INFO if not set
    LOG_FILE_LEVEL: str = Field("INFO", env="LOG_FILE_LEVEL")  # For file handler
    BASE_PATH: str = "/api"  # Default prefix
    OLLAMA_BASE_URL: str
    TOKEN_DB_PATH: str
    CLI_API_KEY_Test: Optional[str] = None

    class Config:
        # env_file = ".env"
        env_file=os.path.join(os.path.dirname(__file__), '..', '.env'),
        env_file_encoding='utf-8'
