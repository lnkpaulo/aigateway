# src/models.py
import os
from pydantic_settings import BaseSettings

# Settings class
class Settings(BaseSettings):
    OLLAMA_BASE_URL: str
    TOKEN_DB_PATH: str
    CLI_API_KEY_Test: str

    class Config:
        # env_file = ".env"
        env_file=os.path.join(os.path.dirname(__file__), '..', '.env'),
        env_file_encoding='utf-8'
