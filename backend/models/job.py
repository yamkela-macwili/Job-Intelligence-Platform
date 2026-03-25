"""Stores job descriptions or predefined roles."""
from sqlalchemy import Column, String, Text, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from core.database import Base


class Job(Base):
    """
    Job model representing job descriptions and requirements.
    
    Attributes:
        id: Unique identifier (UUID)
        title: Job title or role name
        description: Full job description and requirements
        skills_required: JSON array of required skills
        created_at: Timestamp of creation
    """
    
    __tablename__ = "jobs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    skills_required = Column(Text, nullable=True, default="[]")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    __table_args__ = (
        Index("idx_job_title", "title"),
        Index("idx_job_created_at", "created_at"),
    )
    
    def __repr__(self) -> str:
        """String representation of Job object."""
        return f"<Job id={self.id} title={self.title}>"