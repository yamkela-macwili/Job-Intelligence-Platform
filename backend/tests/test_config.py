"""Tests for configuration."""
import pytest
from core.config import settings


class TestSettings:
    """Test configuration settings."""
    
    def test_settings_exists(self):
        """Test that settings object exists."""
        assert settings is not None
    
    def test_database_url_set(self):
        """Test database URL is configured."""
        assert settings.database_url is not None
        assert "postgresql" in settings.database_url.lower() or "sqlite" in settings.database_url.lower()
    
    def test_openai_model_set(self):
        """Test OpenAI model is configured."""
        assert settings.openai_model == "gpt-3.5-turbo"
    
    def test_environment_value(self):
        """Test environment is set."""
        assert settings.environment in ["development", "staging", "production"]
    
    def test_log_level_value(self):
        """Test log level is set."""
        assert settings.log_level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    
    def test_api_title(self):
        """Test API title is configured."""
        assert "Job Intelligence" in settings.api_title
    
    def test_cache_ttl_positive(self):
        """Test cache TTL is positive."""
        assert settings.cache_ttl_hours > 0
