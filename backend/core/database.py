"""Initializes database connection and session management."""
from sqlalchemy import create_engine, event
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.pool import QueuePool, NullPool
from typing import Generator
from core.config import settings
import logging

logger = logging.getLogger(__name__)

# Determine pool class based on database type
# Use NullPool for serverless/temporary connections
pool_class = NullPool if "render" in str(settings.database_url).lower() else QueuePool

# Create database engine with timeout
engine = create_engine(
    settings.database_url,
    pool_class=pool_class,
    pool_size=5 if pool_class == QueuePool else 0,
    max_overflow=10 if pool_class == QueuePool else 0,
    echo=settings.debug,
    connect_args={
        "check_same_thread": False,
        "timeout": 30,  # 30 second connection timeout
    } if "sqlite" in settings.database_url else {
        "connect_timeout": 10,  # 10 second connect timeout for PostgreSQL
        "application_name": "job-intel-api"
    }
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency injection for database session.
    
    Yields:
        Session: Database session object
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Initialize database by creating all tables."""
    try:
        logger.info("Attempting to initialize database...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}", exc_info=True)
        # Don't re-raise - let the app start anyway
        logger.info("Database initialization failed, but app will continue")