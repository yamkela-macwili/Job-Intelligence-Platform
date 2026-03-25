"""Defines structure of AI analysis responses."""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class AnalysisRequest(BaseModel):
    """Schema for analysis request."""
    
    cv_id: UUID = Field(..., description="ID of the CV to analyze")
    job_id: Optional[UUID] = Field(None, description="ID of the job to match (optional)")
    job_description: Optional[str] = Field(None, description="Job description if no job_id")


class SkillGap(BaseModel):
    """Schema for skill gap information."""
    
    skill: str = Field(..., description="Skill name")
    importance: str = Field(..., description="Importance level: high, medium, low")


class Strength(BaseModel):
    """Schema for CV strength."""
    
    skill: str = Field(..., description="Skill name")
    proficiency: str = Field(..., description="Proficiency level: expert, advanced, intermediate, beginner")


class AnalysisResponse(BaseModel):
    """Schema for analysis response."""
    
    id: UUID
    cv_id: UUID
    job_id: Optional[UUID] = None
    match_score: int = Field(..., ge=0, le=100, description="Match score 0-100")
    missing_skills: List[SkillGap] = Field(default_factory=list, description="Skills missing from CV")
    strengths: List[Strength] = Field(default_factory=list, description="CV strengths")
    recommendations: str = Field(..., description="Improvement recommendations")
    roadmap: str = Field(..., description="Career development roadmap")
    created_at: datetime
    
    class Config:
        from_attributes = True


class AnalysisDetailResponse(AnalysisResponse):
    """Detailed analysis response with additional context."""
    
    pass


class CacheHitResponse(BaseModel):
    """Schema for cached analysis response."""
    
    id: UUID
    cached: bool = True
    analysis: AnalysisResponse