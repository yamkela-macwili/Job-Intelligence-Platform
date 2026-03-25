"""Tests for utilities and helpers."""
import pytest
from utils.helpers import (
    parse_json_safely,
    json_to_string,
    clean_text,
    extract_skills_from_text,
    calculate_similarity,
    validate_uuid,
)


class TestJsonUtils:
    """Test JSON utility functions."""
    
    def test_parse_json_safely_valid(self):
        """Test parsing valid JSON."""
        result = parse_json_safely('{"key": "value"}')
        assert result == {"key": "value"}
    
    def test_parse_json_safely_invalid(self):
        """Test parsing invalid JSON returns default."""
        result = parse_json_safely("invalid json", default=[])
        assert result == []
    
    def test_parse_json_safely_none(self):
        """Test parsing None returns default."""
        result = parse_json_safely(None, default={})
        assert result == {}
    
    def test_json_to_string_valid(self):
        """Test converting dict to JSON string."""
        obj = {"key": "value"}
        result = json_to_string(obj)
        assert isinstance(result, str)
        assert "key" in result
    
    def test_json_to_string_list(self):
        """Test converting list to JSON string."""
        obj = ["item1", "item2"]
        result = json_to_string(obj)
        assert isinstance(result, str)
        assert "item1" in result


class TestTextUtils:
    """Test text utility functions."""
    
    def test_clean_text_removes_extra_spaces(self):
        """Test cleaning text removes extra whitespace."""
        text = "Hello    world   test"
        result = clean_text(text)
        assert result == "Hello world test"
    
    def test_clean_text_strips_leading_trailing(self):
        """Test cleaning text removes leading/trailing whitespace."""
        text = "  Hello world  "
        result = clean_text(text)
        assert result == "Hello world"
    
    def test_clean_text_empty_string(self):
        """Test cleaning empty string."""
        result = clean_text("")
        assert result == ""
    
    def test_clean_text_none(self):
        """Test cleaning None returns empty string."""
        result = clean_text(None)
        assert result == ""


class TestSkillExtraction:
    """Test skill extraction functions."""
    
    def test_extract_skills_basic(self):
        """Test basic skill extraction."""
        text = "I know Python, JavaScript, and Java"
        skills = ["Python", "JavaScript", "Java", "C++"]
        result = extract_skills_from_text(text, skills)
        
        assert "Python" in result
        assert "JavaScript" in result
        assert "Java" in result
        assert "C++" not in result
    
    def test_extract_skills_case_insensitive(self):
        """Test skill extraction is case insensitive."""
        text = "I know python and JAVASCRIPT"
        skills = ["Python", "JavaScript"]
        result = extract_skills_from_text(text, skills)
        
        assert len(result) >= 2
    
    def test_extract_skills_empty_list(self):
        """Test extraction with empty skill list."""
        result = extract_skills_from_text("Python", [])
        assert result == []
    
    def test_extract_skills_no_duplicates(self):
        """Test extracted skills have no duplicates."""
        text = "Python Python Python"
        skills = ["Python"]
        result = extract_skills_from_text(text, skills)
        
        assert result.count("Python") == 1


class TestSimilarity:
    """Test similarity calculation."""
    
    def test_similarity_identical_texts(self):
        """Test similarity of identical texts."""
        text = "hello world test"
        result = calculate_similarity(text, text)
        assert result == 1.0
    
    def test_similarity_no_overlap(self):
        """Test similarity of completely different texts."""
        result = calculate_similarity("hello world", "foo bar")
        assert result == 0.0
    
    def test_similarity_partial_overlap(self):
        """Test similarity of partially overlapping texts."""
        result = calculate_similarity("hello world", "hello foo")
        assert 0 < result < 1
    
    def test_similarity_empty_strings(self):
        """Test similarity with empty strings."""
        result = calculate_similarity("", "hello")
        assert result == 0.0


class TestUUIDValidation:
    """Test UUID validation."""
    
    def test_validate_uuid_valid(self):
        """Test validation of valid UUID."""
        valid_uuid = "550e8400-e29b-41d4-a716-446655440000"
        assert validate_uuid(valid_uuid) is True
    
    def test_validate_uuid_invalid(self):
        """Test validation of invalid UUID."""
        assert validate_uuid("not-a-uuid") is False
        assert validate_uuid("") is False
        assert validate_uuid("550e8400") is False
    
    def test_validate_uuid_case_insensitive(self):
        """Test UUID validation is case insensitive."""
        valid_uuid_lower = "550e8400-e29b-41d4-a716-446655440000"
        valid_uuid_upper = "550E8400-E29B-41D4-A716-446655440000"
        
        assert validate_uuid(valid_uuid_lower) is True
        assert validate_uuid(valid_uuid_upper) is True
