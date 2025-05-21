# filepath: c:\Users\adeni\Documents\Works\smart_travel\backend\app\core\config.py
from typing import Optional, Dict, Any
import secrets

from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    
    # Database configuration
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "travel_deals"
    SQLALCHEMY_DATABASE_URI: Optional[str] = None
    
    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    def assemble_db_connection(cls, v: Optional[str], info) -> Any:
        if isinstance(v, str):
            return v
        
        values = info.data
        user = values.get("POSTGRES_USER")
        password = values.get("POSTGRES_PASSWORD")
        host = values.get("POSTGRES_SERVER")
        db = values.get("POSTGRES_DB", "")
        return f"postgresql://{user}:{password}@{host}/{db}"
        
    # CORS configuration
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:3000",      # React default
        "http://localhost:8000",      # API docs when running locally
        "http://127.0.0.1:3000",      # Alternative local React
        "http://127.0.0.1:8000",      # Alternative local API
        "http://localhost:5173",      # Vite default
    ]
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str]:
        """
        Parse a string of comma-separated origins, JSON array string, or list of origins into a list
        This allows flexible configuration from environment variables
        """
        import json
        if isinstance(v, str):
            if v.startswith("[") and v.endswith("]"):
                try:
                    # Try to parse as JSON array
                    return json.loads(v)
                except json.JSONDecodeError:
                    pass
            # If not JSON or JSON parsing failed, try comma-separated format
            return [origin.strip() for origin in v.split(",")]
        if isinstance(v, list):
            return v
        raise ValueError(v)
    
    # Bright Data MCP configuration
    BRIGHT_DATA_API_KEY: str = ""
    BRIGHT_DATA_ZONE_USERNAME: str = ""
    BRIGHT_DATA_ZONE_PASSWORD: str = ""
    # LLM configuration
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.0-flash"
      # JWT settings
    JWT_ALGORITHM: str = "HS256"
      # Application settings
    APP_NAME: str = "Smart Travel API"
    APP_ENVIRONMENT: str = "development"
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    
    # Frontend URL for links in emails
    FRONTEND_URL: str = "http://localhost:3000"
      # Email settings
    EMAILS_FROM_EMAIL: str = "noreply@smarttravel.app"
    EMAILS_FROM_NAME: str = "Smart Travel"
    SMTP_HOST: str = "localhost"  # MailDev server host
    SMTP_PORT: int = 1025         # MailDev SMTP port
    SMTP_USER: str = ""           # No authentication needed for MailDev
    SMTP_PASSWORD: str = ""       # No authentication needed for MailDev
    SMTP_TLS: bool = False        # MailDev doesn't use TLS
    
    model_config = {
        "case_sensitive": True,
        "env_file": ".env",
        "extra": "ignore"
    }


settings = Settings()
