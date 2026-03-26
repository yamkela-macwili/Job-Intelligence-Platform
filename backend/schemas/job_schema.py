from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Any
from datetime import datetime
from uuid import UUID
import json


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

    @field_validator("skills_required", mode="before")
    @classmethod
    def parse_skills(cls, v: Any) -> Any:
        """Parse JSON string to list if needed."""
        if isinstance(v, str):
            try:
                return json.loads(v)
            except (json.JSONDecodeError, TypeError):
                return []
        return v
    
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