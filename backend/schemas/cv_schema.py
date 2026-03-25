"""Defines input/output structure for CV operations."""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class CVBase(BaseModel):
    """Base CV schema with common fields."""
    
    filename: str = Field(..., description="Original filename of the CV")


class CVCreate(CVBase):
    """Schema for creating a new CV."""
    
    raw_text: str = Field(..., description="Extracted text from PDF")


class CVResponse(CVBase):
    """Schema for CV response."""
    
    id: UUID
    raw_text: str
    processed_text: Optional[str] = None
    skills_extracted: Optional[List[str]] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class CVUploadResponse(BaseModel):
    """Schema for CV upload endpoint response."""
    
    id: UUID
    filename: str
    message: str
    created_at: datetime
    
    class Config:
        from_attributes = True