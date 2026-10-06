"""
Configuration module for the Portfolio Flask application.
Loads settings from a .env file using python-dotenv.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration loaded from environment variables."""

    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-to-a-random-secret-key")
    DEBUG = os.getenv("FLASK_DEBUG", "False").lower() in ("true", "1", "yes")

    # Database
    DATABASE_PATH = os.getenv("DATABASE_PATH", "portfolio.db")

    # SMTP Email Settings
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_EMAIL = os.getenv("SMTP_EMAIL", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    NOTIFICATION_EMAIL = os.getenv("NOTIFICATION_EMAIL", "")

    # Admin
    ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "change-this-to-a-secure-key")

    # CV
    CV_FILENAME = os.getenv("CV_FILENAME", "Leroy_Matienga_CV.pdf")

    # Rate Limiting
    RATE_LIMIT_MAX_REQUESTS = int(os.getenv("RATE_LIMIT_MAX_REQUESTS", "5"))
    RATE_LIMIT_WINDOW_SECONDS = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))
