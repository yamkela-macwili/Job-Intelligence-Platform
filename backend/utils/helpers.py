""" Utility functions used across the application."""
import json
import logging
from typing import Any, Dict, List, Optional
import re

logger = logging.getLogger(__name__)


def parse_json_safely(json_str: Optional[str], default: Any = None) -> Any:
    """
    Safely parse JSON string with fallback to default.
    
    Args:
        json_str: JSON string to parse
        default: Default value if parsing fails
        
    Returns:
        Parsed JSON object or default value
    """
    if not json_str:
        return default
    
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError) as e:
        logger.warning(f"Failed to parse JSON: {e}")
        return default


def json_to_string(obj: Any) -> str:
    """
    Convert Python object to JSON string.
    
    Args:
        obj: Object to serialize
        
    Returns:
        JSON string
    """
    try:
        return json.dumps(obj)
    except (TypeError, ValueError) as e:
        logger.error(f"Failed to serialize to JSON: {e}")
        return json.dumps([])


def clean_text(text: str) -> str:
    """
    Clean and normalize text by removing extra whitespace.
    
    Args:
        text: Raw text to clean
        
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove leading/trailing whitespace
    text = text.strip()
    return text


def extract_skills_from_text(text: str, known_skills: Optional[List[str]] = None) -> List[str]:
    """
    Extract skills from text using keyword matching.
    
    Args:
        text: Text to extract skills from
        known_skills: List of known skills to match
        
    Returns:
        List of found skills
    """
    if not text or not known_skills:
        return []
    
    found_skills = []
    text_lower = text.lower()
    
    for skill in known_skills:
        if skill.lower() in text_lower:
            found_skills.append(skill)
    
    return list(set(found_skills))  # Remove duplicates


def calculate_similarity(text1: str, text2: str) -> float:
    """
    Calculate text similarity using simple word overlap.
    
    Args:
        text1: First text
        text2: Second text
        
    Returns:
        Similarity score between 0 and 1
    """
    if not text1 or not text2:
        return 0.0
    
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    if not words1 or not words2:
        return 0.0
    
    intersection = len(words1.intersection(words2))
    union = len(words1.union(words2))
    
    return intersection / union if union > 0 else 0.0


def validate_uuid(uuid_str: str) -> bool:
    """
    Validate UUID format.
    
    Args:
        uuid_str: String to validate
        
    Returns:
        True if valid UUID format
    """
    uuid_pattern = re.compile(
        r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
        re.IGNORECASE
    )
    return bool(uuid_pattern.match(str(uuid_str)))