"""Handles communication with Google Gemini model and generates career insights."""
import logging
import json
import time
from typing import Dict, List, Optional
import google.generativeai as genai
from core.config import settings
from utils.helpers import extract_json_from_text

logger = logging.getLogger(__name__)

class AIEngine:
    """Service for AI-powered analysis using Google Gemini."""

    MAX_RETRIES = 3
    BASE_DELAY = 2  # seconds

    def __init__(self):
        """Initialize the Gemini client."""
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel(settings.gemini_model)
        logger.info(f"AIEngine initialized with model: {settings.gemini_model}")

    def _generate_content(self, prompt: str) -> str:
        """Call Gemini to generate content with retry logic for rate limits."""
        for attempt in range(self.MAX_RETRIES):
            try:
                response = self.model.generate_content(prompt)
                if not response or not response.text:
                    logger.error("Empty response from Gemini")
                    return ""
                return response.text
            except Exception as e:
                error_str = str(e)
                is_rate_limit = "429" in error_str or "quota" in error_str.lower() or "rate" in error_str.lower()
                
                if is_rate_limit and attempt < self.MAX_RETRIES - 1:
                    delay = self.BASE_DELAY * (2 ** attempt)
                    logger.warning(f"Rate limited by Gemini (attempt {attempt + 1}/{self.MAX_RETRIES}). Retrying in {delay}s...")
                    time.sleep(delay)
                    continue
                
                logger.error(f"Error calling Gemini (attempt {attempt + 1}/{self.MAX_RETRIES}): {e}")
                return ""
        return ""

    def analyze_job_match(self, cv_text: str, job_description: str) -> Dict:
        """
        Analyze the match between a CV and a job description.
        
        Args:
            cv_text: Extracted text from CV
            job_description: Full job description
            
        Returns:
            Dict containing match_score, missing_skills, strengths, key_gaps, 
                 recommendations, and suitable_roles.
        """
        try:
            prompt = f"""
Analyze the match between this CV and job description. Provide your response in JSON format.

CV Content:
{cv_text[:3000]}

Job Description:
{job_description[:3000]}

Provide your analysis in this exact JSON format:
{{
    "match_score": <0-100>,
    "missing_skills": [
        {{"skill": "skill_name", "importance": "high/medium/low"}},
    ],
    "strengths": [
        {{"skill": "skill_name", "proficiency": "expert/advanced/intermediate/beginner"}},
    ],
    "key_gaps": ["gap1", "gap2"],
    "recommendations": "Text with specific recommendations",
    "suitable_roles": ["role1", "role2"]
}}
"""
            result_text = self._generate_content(prompt)
            if not result_text:
                raise ValueError("No response from AI")
                
            json_str = extract_json_from_text(result_text)
            result = json.loads(json_str)
            
            logger.info("Successfully completed job match analysis using Gemini")
            return result
            
        except Exception as e:
            logger.error(f"Error in Gemini job match analysis: {e}")
            return {
                "match_score": 0,
                "missing_skills": [],
                "strengths": [],
                "key_gaps": [],
                "recommendations": "Unable to complete analysis at this time",
                "suitable_roles": []
            }

    def generate_career_roadmap(self, cv_text: str, target_role: Optional[str] = None) -> str:
        """
        Generate a detailed career development roadmap based on CV.
        
        Args:
            cv_text: Extracted text from CV
            target_role: Optional target role for specific guidance
            
        Returns:
            Formatted career roadmap text
        """
        try:
            target_context = f"with target role: {target_role}" if target_role else ""
            
            prompt = f"""
Based on this CV {target_context}, create a detailed career development roadmap.

CV Summary:
{cv_text[:3000]}

Provide a comprehensive roadmap in this format:
1. Current Position Analysis
   - Current skills level
   - Current experience gaps
   
2. Short-term Goals (3-6 months)
   - Skills to acquire
   - Projects to undertake
   
3. Medium-term Goals (6-12 months)
   - Career progression steps
   - Certifications to pursue
   
4. Long-term Goals (1-2 years)
   - Target positions
   - Industry transitions
   
5. Learning Resources
   - Recommended courses
   - Books and materials
   
6. Timeline and Milestones
"""
            roadmap = self._generate_content(prompt)
            if not roadmap:
                return "Unable to generate roadmap at this time"
            
            logger.info("Successfully generated career roadmap using Gemini")
            return roadmap
            
        except Exception as e:
            logger.error(f"Error generating roadmap using Gemini: {e}")
            return "Unable to generate roadmap at this time"

    def extract_job_requirements(self, job_description: str) -> Dict:
        """
        Extract structured data from a job description.
        
        Args:
            job_description: Raw job description text
            
        Returns:
            Dict containing skills, experience, and other requirements.
        """
        try:
            prompt = f"""
Extract and structure the requirements from this job description.

Job Description:
{job_description}

Provide your response in this exact JSON format:
{{
    "required_skills": ["skill1", "skill2"],
    "nice_to_have_skills": ["skill1", "skill2"],
    "experience_years": <number>,
    "education_level": "bachelor/master/phd/none",
    "key_responsibilities": ["resp1", "resp2"],
    "salary_range": "range if mentioned",
    "job_level": "entry/mid/senior/lead",
    "required_languages": ["language1"],
    "soft_skills": ["skill1", "skill2"]
}}
"""
            result_text = self._generate_content(prompt)
            if not result_text:
                raise ValueError("No response from AI")
                
            json_str = extract_json_from_text(result_text)
            result = json.loads(json_str)
            
            logger.info("Successfully extracted job requirements using Gemini")
            return result
            
        except Exception as e:
            logger.error(f"Error extracting job requirements using Gemini: {e}")
            return {
                "required_skills": [],
                "nice_to_have_skills": [],
                "experience_years": 0,
                "education_level": "unknown",
                "key_responsibilities": [],
                "salary_range": "unknown",
                "job_level": "unknown",
                "required_languages": [],
                "soft_skills": []
            }

    def generate_recommendations(self, cv_text: str, missing_skills: List[str]) -> str:
        """
        Generate specific actionable improvement recommendations.
        
        Args:
            cv_text: Extracted text from CV
            missing_skills: List of skills to focus on
            
        Returns:
            Formatted recommendations text.
        """
        try:
            skills_text = ", ".join(missing_skills)
            
            prompt = f"""
Based on this CV and the candidate's missing skills, provide specific actionable recommendations.

CV Summary:
{cv_text[:3000]}

Missing Skills: {skills_text}

Provide detailed recommendations covering:
1. Immediate actions (next 1 month)
2. Short-term improvements (1-3 months)
3. Medium-term development (3-6 months)
4. Specific resources and courses
5. Networking and portfolio building suggestions
6. Interview preparation tips
"""
            recommendations = self._generate_content(prompt)
            if not recommendations:
                return "Unable to generate recommendations at this time"
                
            logger.info("Successfully generated recommendations using Gemini")
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations using Gemini: {e}")
            return "Unable to generate recommendations at this time"

# Instance for easy import
AIEngine = AIEngine()
