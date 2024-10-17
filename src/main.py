# main.py
from fastapi import FastAPI
from models import Settings
from libs.token_manager import TokenManager
from routes import router  # Import the router from routes.py
from libs.logger import setup_logging

# Initialize logging
setup_logging()

# Initialize FastAPI app
app = FastAPI()

# Initialize TokenManager and Settings
token_manager = TokenManager()
settings = Settings()

# Include the router with the prefix defined in settings
app.include_router(router, prefix=settings.BASE_PATH)
