import os
from dotenv import load_dotenv

load_dotenv()

def fix_db_url(url: str) -> str:
    """Railway gives postgres:// but SQLAlchemy needs postgresql://"""
    if url and url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql://", 1)
    return url

class Config:
    # PostgreSQL
    SQLALCHEMY_DATABASE_URI = fix_db_url(
        os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/kopihop")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_size": 5,
        "max_overflow": 10,
        "pool_recycle": 300,
    }

    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY", "kopihop-change-this-in-production")
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"

    # Ollama
    OLLAMA_URL   = os.getenv("OLLAMA_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
    USE_OLLAMA   = os.getenv("USE_OLLAMA", "false").lower() == "true"

    # Voice Log
    VOICE_LOG_ENABLED = True