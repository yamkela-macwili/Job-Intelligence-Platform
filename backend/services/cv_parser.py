"""Extracts and cleans text from CV PDFs using pdfplumber."""
import pdfplumber
import spacy
import logging
from typing import List, Tuple, Optional
from utils.helpers import clean_text

logger = logging.getLogger(__name__)

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    logger.warning("spaCy model not found. Install with: python -m spacy download en_core_web_sm")
    nlp = None


class CVParser:
    """Service for parsing and extracting information from CV PDFs."""
    
    @staticmethod
    def extract_text_from_pdf(file_path: str) -> str:
        """
        Extract raw text from PDF file.
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Extracted text from all pages
            
        Raises:
            ValueError: If PDF cannot be read
        """
        try:
            with pdfplumber.open(file_path) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            
            if not text:
                raise ValueError("No text extracted from PDF")
            
            logger.info(f"Successfully extracted text from {file_path}")
            return text
            
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}")
            raise ValueError(f"Failed to parse PDF: {str(e)}")
    
    @staticmethod
    def clean_cv_text(raw_text: str) -> str:
        """
        Clean and normalize CV text.
        
        Args:
            raw_text: Raw extracted text
            
        Returns:
            Cleaned text
        """
        cleaned = clean_text(raw_text)
        # Remove multiple line breaks
        cleaned = "\n".join(line.strip() for line in cleaned.split("\n") if line.strip())
        return cleaned
    
    @staticmethod
    def extract_skills(text: str) -> List[str]:
        """
        Extract skills from CV text using NLP.
        
        Args:
            text: CV text to process
            
        Returns:
            List of extracted skills
        """
        if not nlp:
            logger.warning("spaCy model not loaded, returning empty skills")
            return []
        
        try:
            doc = nlp(text[:1000000])  # Limit text length for performance
            skills = []
            
            # Extract named entities of type ORG, PERSON, GPE
            for ent in doc.ents:
                if ent.label_ in ["ORG", "PRODUCT"]:
                    skills.append(ent.text)
            
            # Common skill keywords
            skill_keywords = {
                "python", "java", "javascript", "typescript", "sql", "react", "angular",
                "vue", "node", "django", "flask", "fastapi", "kubernetes", "docker",
                "aws", "azure", "gcp", "machine learning", "deep learning", "ai",
                "data science", "devops", "microservices", "rest", "graphql",
                "git", "agile", "scrum", "leadership", "communication",
                "c++", "c#", ".net", "golang", "rust", "scala", "r", "matlab",
                "html", "css", "sass", "less", "webpack", "babel", "testing",
                "junit", "pytest", "elasticsearch", "mongodb", "redis", "cassandra",
                "kafka", "rabbitmq", "postgresql", "mysql", "oracle"
            }
            
            text_lower = text.lower()
            for skill in skill_keywords:
                if skill in text_lower:
                    skills.append(skill)
            
            return list(set(skills))  # Remove duplicates
            
        except Exception as e:
            logger.error(f"Error extracting skills: {e}")
            return []
    
    @staticmethod
    def extract_contact_info(text: str) -> dict:
        """
        Extract contact information from CV.
        
        Args:
            text: CV text to process
            
        Returns:
            Dictionary with extracted contact info
        """
        import re
        
        contact_info = {
            "email": None,
            "phone": None,
            "linkedin": None,
            "github": None
        }
        
        try:
            # Extract email
            email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            email_match = re.search(email_pattern, text)
            if email_match:
                contact_info["email"] = email_match.group()
            
            # Extract phone
            phone_pattern = r'\+?1?\d{9,15}'
            phone_match = re.search(phone_pattern, text)
            if phone_match:
                contact_info["phone"] = phone_match.group()
            
            # Extract LinkedIn
            linkedin_pattern = r'(?:https?://)?(?:www\.)?linkedin\.com/in/[\w-]+'
            linkedin_match = re.search(linkedin_pattern, text)
            if linkedin_match:
                contact_info["linkedin"] = linkedin_match.group()
            
            # Extract GitHub
            github_pattern = r'(?:https?://)?(?:www\.)?github\.com/[\w-]+'
            github_match = re.search(github_pattern, text)
            if github_match:
                contact_info["github"] = github_match.group()
            
        except Exception as e:
            logger.error(f"Error extracting contact info: {e}")
        
        return contact_info