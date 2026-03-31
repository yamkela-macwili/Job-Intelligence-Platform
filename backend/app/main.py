"""Entry point of the FastAPI application. Initializes the app and registers routes."""
import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from core.database import init_db
from core.config import settings
from app.api import routes_cv, routes_jobs, routes_analysis

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# CORS origin resolution
# ---------------------------------------------------------------------------
def _resolve_cors_origins() -> list[str]:
    """
    Resolve allowed CORS origins from the CORS_ORIGINS environment variable.

    Accepted formats:
      - "*"                                      → wildcard (dev only)
      - "https://foo.vercel.app"                 → single origin
      - "https://foo.vercel.app,https://bar.com" → comma-separated list

    In production (settings.environment != "development"), a wildcard origin
    is rejected and will raise at startup — forcing an explicit list.
    """
    raw = os.getenv("CORS_ORIGINS", "").strip()

    if not raw:
        if settings.environment == "development":
            logger.warning(
                "CORS_ORIGINS not set. Defaulting to '*' (development only)."
            )
            return ["*"]
        raise RuntimeError(
            "CORS_ORIGINS environment variable is not set. "
            "Set it to a comma-separated list of allowed origins "
            "(e.g. 'https://your-app.vercel.app') before deploying."
        )

    if raw == "*":
        if settings.environment != "development":
            raise RuntimeError(
                "CORS_ORIGINS='*' is not allowed in production. "
                "Specify explicit origins."
            )
        logger.warning("CORS wildcard origin is active — development mode only.")
        return ["*"]

    origins = [o.strip().rstrip("/") for o in raw.split(",") if o.strip()]
    logger.info("CORS allowed origins: %s", origins)
    return origins


CORS_ORIGINS = _resolve_cors_origins()


# ---------------------------------------------------------------------------
# Lifespan (replaces deprecated @app.on_event)
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    logger.info("Starting %s (env=%s, debug=%s)", settings.api_title, settings.environment, settings.debug)
    logger.info("DATABASE_URL configured: %s", bool(os.getenv("DATABASE_URL")))
    try:
        init_db()
        logger.info("Database initialised successfully.")
    except Exception as exc:
        # Non-fatal: app starts but DB-dependent routes will fail gracefully
        logger.warning("Database initialisation failed (non-blocking): %s", str(exc)[:200])

    yield  # application runs here

    # --- Shutdown ---
    logger.info("Shutting down %s.", settings.api_title)


# ---------------------------------------------------------------------------
# App factory
# ---------------------------------------------------------------------------
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version="1.0.0",
    docs_url="/docs" if settings.environment != "production" else None,   # hide docs in prod
    redoc_url="/redoc" if settings.environment != "production" else None,
    openapi_url="/openapi.json" if settings.environment != "production" else None,
    lifespan=lifespan,
)


# ---------------------------------------------------------------------------
# Middleware
# IMPORTANT: CORSMiddleware must be registered FIRST.
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    # allow_credentials MUST be False when allow_origins includes "*"
    # (browsers reject credentialed requests to wildcard origins).
    allow_credentials="*" not in CORS_ORIGINS,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID"],
    max_age=600,
)


# ---------------------------------------------------------------------------
# Exception handlers
# ---------------------------------------------------------------------------
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Return structured 422 with field-level errors. Never expose raw body in production."""
    logger.warning("Validation error for %s: %s", request.url, exc.errors())
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
            # Only include the raw body in non-production environments
            **({"body": exc.body} if settings.environment != "production" else {}),
        },
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch-all handler. Never leak internal details in production."""
    logger.error("Unhandled exception on %s: %s", request.url, exc, exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            # Only expose raw error message outside production
            **({"error": str(exc)} if settings.debug else {}),
        },
    )


# ---------------------------------------------------------------------------
# Health / readiness endpoints
# ---------------------------------------------------------------------------
@app.get("/health", tags=["Health"], include_in_schema=False)
async def health_check():
    """Liveness probe — returns 200 if the process is running."""
    return {"status": "ok", "service": settings.api_title, "version": "1.0.0"}


@app.get("/ready", tags=["Health"], include_in_schema=False)
async def ready_check():
    """
    Readiness probe for Kubernetes / Render health checks.
    Extend this to verify DB connectivity if needed.
    """
    db_url_set = bool(os.getenv("DATABASE_URL"))
    return {
        "ready": True,
        "service": settings.api_title,
        "database_configured": db_url_set,
    }


# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(routes_cv.router,       prefix="/api/v1/cv",       tags=["CV Operations"])
app.include_router(routes_jobs.router,     prefix="/api/v1/jobs",     tags=["Job Management"])
app.include_router(routes_analysis.router, prefix="/api/v1/analysis", tags=["AI Analysis"])


@app.get("/", tags=["Root"], include_in_schema=False)
async def root():
    return {
        "service": settings.api_title,
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "health": "/health",
            "cv":       "/api/v1/cv",
            "jobs":     "/api/v1/jobs",
            "analysis": "/api/v1/analysis",
        },
    }


# ---------------------------------------------------------------------------
# Local dev entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",           # string form enables --reload
        host="0.0.0.0",
        port=8000,
        log_level=settings.log_level.lower(),
        reload=settings.environment == "development",
    )