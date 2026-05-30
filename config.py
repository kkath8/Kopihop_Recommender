"""
config.py — KopiHop Configuration
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # PostgreSQL
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:Kath-PostgreSQL@localhost:5432/kopihop"
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
    DEBUG = os.getenv("DEBUG", "true").lower() == "true"

    OLLAMA_URL     = os.getenv("OLLAMA_URL", "http://localhost:11434")
    OLLAMA_MODEL   = os.getenv("OLLAMA_MODEL", "llama3")   # or "mistral", "phi3"
    USE_OLLAMA     = os.getenv("USE_OLLAMA", "true").lower() == "true"

    # Voice Log
    VOICE_LOG_ENABLED = True
