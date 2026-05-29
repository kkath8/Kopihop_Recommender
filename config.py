import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # PostgreSQL connection
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:password@localhost:5432/cafe_recommender"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Anthropic API
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY", "cafe-recommender-secret-key")
    DEBUG = os.getenv("DEBUG", "true").lower() == "true"
