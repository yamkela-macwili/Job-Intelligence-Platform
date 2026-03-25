"""Tests for API health check endpoint."""
import pytest
from fastapi.testclient import TestClient
from app.main import app


class TestHealth:
    """Test health check endpoint."""
    
    @pytest.fixture
    def client(self):
        """Get test client."""
        return TestClient(app)
    
    def test_health_check(self, client):
        """Test health endpoint returns OK status."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "OK"
        assert "service" in response.json()
        assert "version" in response.json()
    
    def test_health_check_structure(self, client):
        """Test health check response structure."""
        response = client.get("/health")
        data = response.json()
        
        assert "status" in data
        assert "service" in data
        assert "version" in data
        assert data["status"] in ["OK", "UP"]


class TestDocumentation:
    """Test API documentation endpoints."""
    
    @pytest.fixture
    def client(self):
        """Get test client."""
        return TestClient(app)
    
    def test_swagger_ui_available(self, client):
        """Test Swagger UI is available."""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "swagger" in response.text.lower() or "openapi" in response.text.lower()
    
    def test_redoc_available(self, client):
        """Test ReDoc is available."""
        response = client.get("/redoc")
        assert response.status_code == 200
        assert "redoc" in response.text.lower()
    
    def test_openapi_schema(self, client):
        """Test OpenAPI schema endpoint."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
        assert "paths" in schema
