import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration class."""
    TELEX_WEBHOOK = os.getenv("TELEX_WEBHOOK")
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    GITHUB_REPO = os.getenv("GITHUB_REPO")
    FLASK_ENV = os.getenv("FLASK_ENV", "production")
    PORT = int(os.getenv("PORT", 5000))

# Create an instance of Config
config = Config()
