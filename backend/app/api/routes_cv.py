"""Handles CV upload and processing endpoints."""
import logging
import os
import tempfile
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from core.database import get_db
from core.config import settings
from models.cv import CV
from schemas.cv_schema import CVResponse, CVUploadResponse
from services.cv_parser import CVParser
from utils.helpers import json_to_string

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/upload", response_model=CVUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_cv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload and process a CV PDF file.
    
    Args:
        file: PDF file upload
        db: Database session
        
    Returns:
        CVUploadResponse with CV details and ID
        
    Raises:
        HTTPException: If file is invalid or processing fails
    """
    # Validate file type
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are accepted"
        )
    
    # Validate file size
    file_content = await file.read()
    if len(file_content) > settings.max_upload_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds maximum allowed size of {settings.max_upload_size} bytes"
        )
    
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(file_content)
            tmp_path = tmp_file.name
        
        # Extract text from PDF
        raw_text = CVParser.extract_text_from_pdf(tmp_path)
        
        # Clean text
        processed_text = CVParser.clean_cv_text(raw_text)
        
        # Extract skills
        skills = CVParser.extract_skills(raw_text)
        skills_json = json_to_string(skills)
        
        # Create CV record in database
        cv = CV(
            filename=file.filename,
            raw_text=raw_text,
            processed_text=processed_text,
            skills_extracted=skills_json
        )
        
        db.add(cv)
        db.commit()
        db.refresh(cv)
        
        # Clean up temporary file
        os.remove(tmp_path)
        
        logger.info(f"CV uploaded successfully: {cv.id}")
        
        return CVUploadResponse(
            id=cv.id,
            filename=cv.filename,
            message="CV uploaded and processed successfully",
            created_at=cv.created_at
        )
        
    except ValueError as e:
        logger.error(f"CV parsing error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error uploading CV: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing CV file"
        )


@router.get("/{cv_id}", response_model=CVResponse)
async def get_cv(
    cv_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific CV by ID.
    
    Args:
        cv_id: CV UUID
        db: Database session
        
    Returns:
        CVResponse with CV details
        
    Raises:
        HTTPException: If CV not found
    """
    cv = db.query(CV).filter(CV.id == cv_id).first()
    
    if not cv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CV not found"
        )
    
    return cv


@router.get("", response_model=list[CVResponse])
async def list_cvs(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    List all uploaded CVs with pagination.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
        
    Returns:
        List of CVs
    """
    if limit > 100:
        limit = 100
    if skip < 0:
        skip = 0
    
    cvs = db.query(CV).offset(skip).limit(limit).all()
    return cvs


@router.delete("/{cv_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cv(
    cv_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Delete a CV record.
    
    Args:
        cv_id: CV UUID
        db: Database session
        
    Raises:
        HTTPException: If CV not found
    """
    cv = db.query(CV).filter(CV.id == cv_id).first()
    
    if not cv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CV not found"
        )
    
    db.delete(cv)
    db.commit()
    
    logger.info(f"CV deleted: {cv_id}")
    return None