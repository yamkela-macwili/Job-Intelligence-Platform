"""Handles AI analysis requests and responses."""
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from uuid import UUID
from datetime import datetime, timedelta

from core.database import get_db
from core.config import settings
from models.cv import CV
from models.job import Job
from models.analysis import Analysis
from schemas.analysis_schema import AnalysisRequest, AnalysisResponse, SkillGap, Strength
from services.cv_parser import CVParser
from services.ai_engine import AIEngine
from services.job_matcher import JobMatcher
from services.roadmap_generator import RoadmapGenerator
from utils.helpers import parse_json_safely, json_to_string

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("", response_model=AnalysisResponse, status_code=status.HTTP_201_CREATED)
async def create_analysis(
    request: AnalysisRequest,
    db: Session = Depends(get_db)
):
    """
    Perform AI-powered analysis on CV-Job match.
    
    Args:
        request: Analysis request with cv_id and job_id or job_description
        db: Database session
        
    Returns:
        AnalysisResponse with analysis results
        
    Raises:
        HTTPException: If CV or Job not found or analysis fails
    """
    # Validate CV exists
    cv = db.query(CV).filter(CV.id == request.cv_id).first()
    if not cv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CV not found"
        )
    
    job_id = None
    job_description = None
    
    if request.job_id:
        # Validate job exists
        job = db.query(Job).filter(Job.id == request.job_id).first()
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found"
            )
        job_id = request.job_id
        job_description = job.description
    elif request.job_description:
        job_description = request.job_description
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either job_id or job_description must be provided"
        )
    
    try:
        # Check cache for similar analysis
        cached_analysis = _check_cache(db, request.cv_id, job_id, job_description)
        if cached_analysis:
            logger.info(f"Returning cached analysis: {cached_analysis.id}")
            return _format_analysis_response(cached_analysis)
        
        # Perform comprehensive AI analysis
        ai_analysis = AIEngine.analyze_job_match(cv.raw_text, job_description)
        
        match_score = ai_analysis.get("match_score", 0)
        missing_skills = ai_analysis.get("missing_skills", [])
        strengths = ai_analysis.get("strengths", [])
        key_gaps = ai_analysis.get("key_gaps", [])
        suitable_roles = ai_analysis.get("suitable_roles", [])
        recommendations = ai_analysis.get("recommendations", "No recommendations available")
        
        # Generate roadmap
        roadmap = AIEngine.generate_career_roadmap(cv.raw_text, None)
        
        # Store analysis in database
        analysis = Analysis(
            cv_id=request.cv_id,
            job_id=job_id,
            match_score=match_score,
            missing_skills=json_to_string(missing_skills),
            strengths=json_to_string(strengths),
            key_gaps=json_to_string(key_gaps),
            suitable_roles=json_to_string(suitable_roles),
            recommendations=recommendations,
            roadmap=roadmap
        )
        
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        
        logger.info(f"Analysis completed: {analysis.id} with score {match_score}")
        
        return _format_analysis_response(analysis)
        
    except Exception as e:
        logger.error(f"Error during analysis: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error performing analysis"
        )


@router.get("/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis(
    analysis_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific analysis by ID.
    
    Args:
        analysis_id: Analysis UUID
        db: Database session
        
    Returns:
        AnalysisResponse with analysis details
        
    Raises:
        HTTPException: If analysis not found
    """
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    return _format_analysis_response(analysis)


@router.get("", response_model=list[AnalysisResponse])
async def list_analyses(
    cv_id: UUID | None = None,
    job_id: UUID | None = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    List analyses with optional filtering.
    
    Args:
        cv_id: Filter by CV ID (optional)
        job_id: Filter by Job ID (optional)
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
        
    Returns:
        List of analyses
    """
    if limit > 100:
        limit = 100
    if skip < 0:
        skip = 0
    
    query = db.query(Analysis)
    
    if cv_id:
        query = query.filter(Analysis.cv_id == cv_id)
    if job_id:
        query = query.filter(Analysis.job_id == job_id)
    
    analyses = query.offset(skip).limit(limit).all()
    
    return [_format_analysis_response(a) for a in analyses]


@router.delete("/{analysis_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_analysis(
    analysis_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Delete an analysis record.
    
    Args:
        analysis_id: Analysis UUID
        db: Database session
        
    Raises:
        HTTPException: If analysis not found
    """
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    db.delete(analysis)
    db.commit()
    
    logger.info(f"Analysis deleted: {analysis_id}")
    return None


# Helper functions

def _check_cache(db: Session, cv_id: UUID, job_id: UUID | None, job_description: str) -> Analysis | None:
    """
    Check if similar analysis exists in cache within TTL.
    
    Args:
        db: Database session
        cv_id: CV ID
        job_id: Job ID (optional)
        job_description: Job description text
        
    Returns:
        Cached analysis if found, None otherwise
    """
    # Calculate cache expiry time
    cache_expiry = datetime.utcnow() - timedelta(hours=settings.cache_ttl_hours)
    
    # Query for similar analysis
    query = db.query(Analysis).filter(
        and_(
            Analysis.cv_id == cv_id,
            Analysis.created_at >= cache_expiry
        )
    )
    
    if job_id:
        query = query.filter(Analysis.job_id == job_id)
    
    # Return first match
    return query.first()


def _format_analysis_response(analysis: Analysis) -> AnalysisResponse:
    """
    Format analysis database record to response schema.
    
    Args:
        analysis: Analysis database record
        
    Returns:
        AnalysisResponse
    """
    missing_skills_data = parse_json_safely(analysis.missing_skills, [])
    strengths_data = parse_json_safely(analysis.strengths, [])
    key_gaps = parse_json_safely(analysis.key_gaps, [])
    suitable_roles = parse_json_safely(analysis.suitable_roles, [])
    
    # Parse roadmap - try to parse as JSON first, otherwise keep as string
    roadmap_data = analysis.roadmap
    try:
        roadmap_data = parse_json_safely(analysis.roadmap, analysis.roadmap)
    except:
        pass  # If parsing fails, keep original roadmap string
    
    # Convert to SkillGap objects
    missing_skills = [
        SkillGap(skill=s["skill"], importance=s["importance"])
        for s in missing_skills_data
    ]
    
    # Convert to Strength objects
    strengths = [
        Strength(skill=s["skill"], proficiency=s["proficiency"])
        for s in strengths_data
    ]
    
    return AnalysisResponse(
        id=analysis.id,
        cv_id=analysis.cv_id,
        job_id=analysis.job_id,
        match_score=analysis.match_score,
        missing_skills=missing_skills,
        strengths=strengths,
        key_gaps=key_gaps,
        suitable_roles=suitable_roles,
        recommendations=analysis.recommendations,
        roadmap=roadmap_data,
        created_at=analysis.created_at
    )