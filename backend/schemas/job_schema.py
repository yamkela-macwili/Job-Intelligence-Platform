""" Defines job related request and response formats."""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class JobBase(BaseModel):
    """Base job schema with common fields."""
    
    title: str = Field(..., min_length=1, max_length=255, description="Job title or role name")
    description: str = Field(..., min_length=1, description="Full job description")


class JobCreate(JobBase):
    """Schema for creating a new job."""
    
    pass


class JobResponse(JobBase):
    """Schema for job response."""
    
    id: UUID
    skills_required: Optional[List[str]] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class JobUploadResponse(BaseModel):
    """Schema for job upload endpoint response."""
    
    id: UUID
    title: str
    message: str
    created_at: datetime
    
    class Config:
        from_attributes = True