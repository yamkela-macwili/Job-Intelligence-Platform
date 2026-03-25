"""Handles communication with AI models and generates insights."""
import logging
import json
from typing import Dict, List, Optional
from openai import OpenAI
from core.config import settings
from utils.helpers import parse_json_safely, json_to_string

logger = logging.getLogger(__name__)


class AIEngine:
    """Service for AI-powered analysis using OpenAI."""
    
    MODEL = settings.openai_model
    
    @staticmethod
    def _get_client() -> OpenAI:
        """Get OpenAI client instance."""
        return OpenAI(api_key=settings.openai_api_key)
    
    @staticmethod
    def analyze_job_match(cv_text: str, job_description: str) -> Dict:
        """
        Analyze job match between CV and job description using AI.
        
        Args:
            cv_text: Extracted CV text
            job_description: Job description text
            
        Returns:
            Dictionary with match analysis results
        """
        try:
            prompt = f"""
Analyze the match between this CV and job description. Provide your response in JSON format.

CV Content:
{cv_text[:2000]}

Job Description:
{job_description[:2000]}

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
            
            response = AIEngine._get_client().chat.completions.create(
                model=AIEngine.MODEL,
                messages=[
                    {"role": "system", "content": "You are an expert career analyst and HR professional."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            result_text = response.choices[0].message.content
            result = json.loads(result_text)
            
            logger.info("Successfully completed job match analysis")
            return result
            
        except Exception as e:
            logger.error(f"Error in job match analysis: {e}")
            return {
                "match_score": 0,
                "missing_skills": [],
                "strengths": [],
                "key_gaps": [],
                "recommendations": "Unable to complete analysis",
                "suitable_roles": []
            }
    
    @staticmethod
    def generate_career_roadmap(cv_text: str, target_role: Optional[str] = None) -> str:
        """
        Generate career development roadmap using AI.
        
        Args:
            cv_text: Extracted CV text
            target_role: Optional target role
            
        Returns:
            Structured career roadmap text
        """
        try:
            target_context = f"with target role: {target_role}" if target_role else ""
            
            prompt = f"""
Based on this CV {target_context}, create a detailed career development roadmap.

CV Summary:
{cv_text[:2000]}

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
            
            response = AIEngine._get_client().chat.completions.create(
                model=AIEngine.MODEL,
                messages=[
                    {"role": "system", "content": "You are an expert career coach and mentoring professional."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            roadmap = response.choices[0].message.content
            logger.info("Successfully generated career roadmap")
            return roadmap
            
        except Exception as e:
            logger.error(f"Error generating roadmap: {e}")
            return "Unable to generate roadmap at this time"
    
    @staticmethod
    def extract_job_requirements(job_description: str) -> Dict:
        """
        Extract structured requirements from job description using AI.
        
        Args:
            job_description: Job description text
            
        Returns:
            Dictionary with structured requirements
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
            
            response = AIEngine._get_client().chat.completions.create(
                model=AIEngine.MODEL,
                messages=[
                    {"role": "system", "content": "You are an expert in job analysis and requirements extraction."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=1000
            )
            
            result_text = response.choices[0].message.content
            result = json.loads(result_text)
            
            logger.info("Successfully extracted job requirements")
            return result
            
        except Exception as e:
            logger.error(f"Error extracting job requirements: {e}")
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
    
    @staticmethod
    def generate_recommendations(cv_text: str, missing_skills: List[str]) -> str:
        """
        Generate personalized improvement recommendations.
        
        Args:
            cv_text: Extracted CV text
            missing_skills: List of missing skills
            
        Returns:
            Detailed recommendations text
        """
        try:
            skills_text = ", ".join(missing_skills)
            
            prompt = f"""
Based on this CV and the candidate's missing skills, provide specific actionable recommendations.

CV Summary:
{cv_text[:2000]}

Missing Skills: {skills_text}

Provide detailed recommendations covering:
1. Immediate actions (next 1 month)
2. Short-term improvements (1-3 months)
3. Medium-term development (3-6 months)
4. Specific resources and courses
5. Networking and portfolio building suggestions
6. Interview preparation tips
"""
            
            response = AIEngine._get_client().chat.completions.create(
                model=AIEngine.MODEL,
                messages=[
                    {"role": "system", "content": "You are an expert career coach providing personalized career development advice."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            recommendations = response.choices[0].message.content
            logger.info("Successfully generated recommendations")
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return "Unable to generate recommendations at this time"