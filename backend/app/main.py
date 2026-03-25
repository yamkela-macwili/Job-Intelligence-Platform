"""Entry point of the FastAPI application. Initializes the app and registers routes."""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from core.database import init_db
from core.config import settings
from app.api import routes_cv, routes_jobs, routes_analysis

# Configure logging
logging.basicConfig(
    level=settings.log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Custom exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handle all exceptions globally."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error": str(exc) if settings.debug else "An error occurred"
        }
    )


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database and log startup."""
    logger.info(f"Starting {settings.api_title}")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Debug: {settings.debug}")
    
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.warning(f"Failed to initialize database (non-blocking): {e}")
        logger.info("Application will continue without database initialization")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Log shutdown."""
    logger.info(f"Shutting down {settings.api_title}")


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        status: OK if service is healthy
    """
    return {
        "status": "OK",
        "service": settings.api_title,
        "version": "1.0.0"
    }


# Ready check endpoint
@app.get("/ready", tags=["Health"])
async def ready_check():
    """
    Readiness check endpoint for Kubernetes.
    
    Returns:
        ready: True if service is ready to handle requests
    """
    return {
        "ready": True,
        "service": settings.api_title
    }


# Include routers
app.include_router(
    routes_cv.router,
    prefix="/api/v1/cv",
    tags=["CV Operations"]
)

app.include_router(
    routes_jobs.router,
    prefix="/api/v1/jobs",
    tags=["Job Management"]
)

app.include_router(
    routes_analysis.router,
    prefix="/api/v1/analysis",
    tags=["AI Analysis"]
)


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with API information.
    
    Returns:
        API information and available endpoints
    """
    return {
        "message": "Welcome to Job Intelligence Platform API",
        "version": "1.0.0",
        "documentation": "/docs",
        "endpoints": {
            "health": "/health",
            "cv": "/api/v1/cv",
            "jobs": "/api/v1/jobs",
            "analysis": "/api/v1/analysis"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level=settings.log_level.lower()
    )