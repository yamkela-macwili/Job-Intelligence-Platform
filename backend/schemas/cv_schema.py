from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Any
from datetime import datetime
from uuid import UUID
import json


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

    @field_validator("skills_extracted", mode="before")
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


class CVUploadResponse(BaseModel):
    """Schema for CV upload endpoint response."""
    
    id: UUID
    filename: str
    message: str
    created_at: datetime
    
    class Config:
        from_attributes = True