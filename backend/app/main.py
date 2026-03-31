"""Entry point of the FastAPI application. Initializes the app and registers routes."""
import logging
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
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
cors_origins = os.getenv("CORS_ORIGINS", "").split(",") if os.getenv("CORS_ORIGINS") else ["*"]
cors_origins = [origin.strip() for origin in cors_origins if origin.strip()]

logger.info(f"CORS origins configured: {cors_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=[
        "Content-Type",
        "Authorization",
        "Accept",
        "Origin",
        "Access-Control-Request-Method",
        "Access-Control-Request-Headers",
    ],
    expose_headers=["*"],
    max_age=3600,
)


# Custom exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """Log detailed validation errors."""
    logger.error(f"Validation error for {request.url}: {exc.errors()}")
    logger.error(f"Request body: {exc.body}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body}
    )


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
    logger.info(f"Database URL configured: {'Yes' if os.getenv('DATABASE_URL') else 'No'}")
    
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.warning(f"Failed to initialize database (non-blocking): {str(e)[:200]}")
        logger.info("Application will continue without database initialization")
        logger.info("Features requiring database may not work until connection is restored")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Log shutdown."""
    logger.info(f"Shutting down {settings.api_title}")


# CORS test endpoint
@app.options("/{full_path:path}", tags=["CORS"])
async def options_handler(full_path: str):
    """Handle CORS preflight requests."""
    return {"message": "CORS preflight OK"}


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