"""Tests for database models."""
import pytest
from uuid import uuid4
from datetime import datetime
from models.cv import CV
from models.job import Job
from models.analysis import Analysis


class TestCVModel:
    """Test CV model."""
    
    def test_cv_repr(self):
        """Test CV string representation."""
        cv = CV(filename="test.pdf", raw_text="test")
        repr_str = repr(cv)
        
        assert "CV" in repr_str
        assert "test.pdf" in repr_str


class TestJobModel:
    """Test Job model."""
    
    def test_job_repr(self):
        """Test Job string representation."""
        job = Job(title="Developer", description="Job desc")
        repr_str = repr(job)
        
        assert "Job" in repr_str
        assert "Developer" in repr_str


class TestAnalysisModel:
    """Test Analysis model."""
    
    def test_analysis_repr(self):
        """Test Analysis string representation."""
        analysis = Analysis(
            cv_id=uuid4(),
            job_id=uuid4(),
            match_score=80
        )
        repr_str = repr(analysis)
        
        assert "Analysis" in repr_str
        assert "80" in repr_str
