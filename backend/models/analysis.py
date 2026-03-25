""" Stores analysis results such as match scores and insights."""
from sqlalchemy import Column, String, Text, DateTime, Integer, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from core.database import Base


class Analysis(Base):
    """
    Analysis model storing AI-powered analysis results.
    
    Attributes:
        id: Unique identifier (UUID)
        cv_id: Foreign key to CV
        job_id: Foreign key to Job (nullable for general analysis)
        match_score: Numeric score 0-100 representing job match
        missing_skills: JSON array of skills CV is missing
        strengths: JSON array of CV strengths
        recommendations: Text recommendations for improvement
        roadmap: Structured career development roadmap
        created_at: Timestamp of analysis creation
    """
    
    __tablename__ = "analyses"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    cv_id = Column(UUID(as_uuid=True), ForeignKey("cvs.id"), nullable=False, index=True)
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id"), nullable=True, index=True)
    match_score = Column(Integer, nullable=False, default=0)
    missing_skills = Column(Text, nullable=True, default="[]")
    strengths = Column(Text, nullable=True, default="[]")
    recommendations = Column(Text, nullable=True)
    roadmap = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    __table_args__ = (
        Index("idx_analysis_cv_id", "cv_id"),
        Index("idx_analysis_job_id", "job_id"),
        Index("idx_analysis_created_at", "created_at"),
    )
    
    def __repr__(self) -> str:
        """String representation of Analysis object."""
        return f"<Analysis id={self.id} cv_id={self.cv_id} match_score={self.match_score}>"