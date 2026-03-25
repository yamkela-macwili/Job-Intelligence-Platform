"""Handles job input or predefined job roles."""
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from core.database import get_db
from models.job import Job
from schemas.job_schema import JobCreate, JobResponse, JobUploadResponse
from services.ai_engine import AIEngine
from utils.helpers import json_to_string

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("", response_model=JobUploadResponse, status_code=status.HTTP_201_CREATED)
async def create_job(
    job: JobCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new job entry.
    
    Args:
        job: Job creation payload
        db: Database session
        
    Returns:
        JobUploadResponse with job details
        
    Raises:
        HTTPException: If job creation fails
    """
    try:
        # Extract skills from job description using AI
        job_requirements = AIEngine.extract_job_requirements(job.description)
        skills_json = json_to_string(job_requirements.get("required_skills", []))
        
        # Create job record
        new_job = Job(
            title=job.title,
            description=job.description,
            skills_required=skills_json
        )
        
        db.add(new_job)
        db.commit()
        db.refresh(new_job)
        
        logger.info(f"Job created successfully: {new_job.id}")
        
        return JobUploadResponse(
            id=new_job.id,
            title=new_job.title,
            message="Job created successfully",
            created_at=new_job.created_at
        )
        
    except Exception as e:
        logger.error(f"Error creating job: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating job entry"
        )


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific job by ID.
    
    Args:
        job_id: Job UUID
        db: Database session
        
    Returns:
        JobResponse with job details
        
    Raises:
        HTTPException: If job not found
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    return job


@router.get("", response_model=list[JobResponse])
async def list_jobs(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    List all jobs with pagination.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
        
    Returns:
        List of jobs
    """
    if limit > 100:
        limit = 100
    if skip < 0:
        skip = 0
    
    jobs = db.query(Job).offset(skip).limit(limit).all()
    return jobs


@router.put("/{job_id}", response_model=JobResponse)
async def update_job(
    job_id: UUID,
    job_update: JobCreate,
    db: Session = Depends(get_db)
):
    """
    Update an existing job entry.
    
    Args:
        job_id: Job UUID
        job_update: Updated job data
        db: Database session
        
    Returns:
        Updated JobResponse
        
    Raises:
        HTTPException: If job not found
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    try:
        job.title = job_update.title
        job.description = job_update.description
        
        # Re-extract skills
        job_requirements = AIEngine.extract_job_requirements(job_update.description)
        job.skills_required = json_to_string(job_requirements.get("required_skills", []))
        
        db.commit()
        db.refresh(job)
        
        logger.info(f"Job updated: {job_id}")
        
        return job
        
    except Exception as e:
        logger.error(f"Error updating job: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating job"
        )


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(
    job_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Delete a job record.
    
    Args:
        job_id: Job UUID
        db: Database session
        
    Raises:
        HTTPException: If job not found
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    db.delete(job)
    db.commit()
    
    logger.info(f"Job deleted: {job_id}")
    return None