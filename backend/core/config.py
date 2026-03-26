"""Manages environment variables and application settings."""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database Configuration
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@localhost:5432/job_intelligence"
    )
    
    # Gemini Configuration
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    
    # Application Configuration
    environment: str = os.getenv("ENVIRONMENT", "development")
    debug: bool = os.getenv("DEBUG", "True").lower() == "true"
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    # API Configuration
    api_version: str = "v1"
    api_title: str = "Job Intelligence Platform API"
    api_description: str = "AI-powered career and job intelligence platform"
    
    # File Upload Configuration
    max_upload_size: int = 50 * 1024 * 1024  # 50MB
    upload_directory: str = "/tmp/uploads"
    
    # Cache Configuration
    cache_ttl_hours: int = 24
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()