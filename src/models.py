from pydantic_settings import BaseSettings

# Settings class
class Settings(BaseSettings):
    OLLAMA_BASE_URL: str
    TOKEN_DB_PATH: str

    class Config:
        env_file = ".env"