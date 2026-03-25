"""Defines the CV table schema."""
from sqlalchemy import Column, String, Text, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from core.database import Base


class CV(Base):
    """
    CV model representing uploaded curriculum vitae documents.
    
    Attributes:
        id: Unique identifier (UUID)
        filename: Original filename of uploaded PDF
        raw_text: Extracted text content from PDF
        processed_text: Cleaned and normalized text
        skills_extracted: JSON array of extracted skills
        created_at: Timestamp of creation
    """
    
    __tablename__ = "cvs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    filename = Column(String(255), nullable=False)
    raw_text = Column(Text, nullable=False)
    processed_text = Column(Text, nullable=True)
    skills_extracted = Column(Text, nullable=True, default="[]")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    __table_args__ = (
        Index("idx_cv_created_at", "created_at"),
    )
    
    def __repr__(self) -> str:
        """String representation of CV object."""
        return f"<CV id={self.id} filename={self.filename}>"