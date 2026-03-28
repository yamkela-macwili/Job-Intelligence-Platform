"""Handles communication with Azure AI Projects Agent and generates career insights."""
import logging
import json
import time
from typing import Dict, List, Optional
from openai import AzureOpenAI
from core.config import settings
from utils.helpers import extract_json_from_text

logger = logging.getLogger(__name__)

class AIEngine:
    """Service for AI-powered analysis using Azure OpenAI."""

    MAX_RETRIES = 3
    BASE_DELAY = 2  # seconds

    def __init__(self):
        """Initialize the Azure OpenAI client."""
        try:
            self.client = AzureOpenAI(
                api_key=settings.azure_ai_api_key,
                api_version="2024-02-15-preview",
                azure_endpoint=settings.azure_ai_endpoint
            )
            logger.info("Azure OpenAI client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Azure OpenAI client: {e}")
            self.client = None

    def _generate_content(self, prompt: str) -> str:
        """Call Azure OpenAI to generate content with retry logic for rate limits."""
        if not self.client:
            logger.error("Azure OpenAI client not initialized")
            return ""
            
        for attempt in range(self.MAX_RETRIES):
            try:
                response = self.client.chat.completions.create(
                    model=settings.azure_ai_model_deployment_name,
                    messages=[
                        {"role": "system", "content": "You are an expert career intelligence AI. You analyze resumes and job descriptions to provide precise JSON evaluations. Output ONLY valid JSON where explicitly requested."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=2000
                )
                
                if not response or not response.choices:
                    logger.error("Empty response from Azure OpenAI")
                    return ""
                
                return response.choices[0].message.content
            except Exception as e:
                error_str = str(e)
                is_rate_limit = "429" in error_str or "quota" in error_str.lower() or "rate" in error_str.lower()
                
                if is_rate_limit and attempt < self.MAX_RETRIES - 1:
                    delay = self.BASE_DELAY * (2 ** attempt)
                    logger.warning(f"Rate limited by Azure OpenAI (attempt {attempt + 1}/{self.MAX_RETRIES}). Retrying in {delay}s...")
                    time.sleep(delay)
                    continue
                
                logger.error(f"Error calling Azure OpenAI (attempt {attempt + 1}/{self.MAX_RETRIES}): {e}")
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
            
            logger.info("Successfully completed job match analysis using Azure OpenAI")
            return result
            
        except Exception as e:
            logger.error(f"Error in Azure OpenAI job match analysis: {e}")
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
            Formatted career roadmap as JSON string
        """
        try:
            target_context = f"with target role: {target_role}" if target_role else ""
            
            prompt = f"""
Based on this CV {target_context}, create a detailed career development roadmap in JSON format.

CV Summary:
{cv_text[:3000]}

Provide a comprehensive roadmap in this exact JSON format:
{{
    "current_position_analysis": {{
        "current_skills": ["skill1", "skill2"],
        "experience_gaps": ["gap1", "gap2"]
    }},
    "short_term_goals": {{
        "timeline": "3-6 months",
        "skills_to_acquire": ["skill1", "skill2"],
        "projects": ["project1", "project2"]
    }},
    "medium_term_goals": {{
        "timeline": "6-12 months",
        "career_progression": ["step1", "step2"],
        "certifications": ["cert1", "cert2"]
    }},
    "long_term_goals": {{
        "timeline": "1-2 years",
        "target_positions": ["role1", "role2"],
        "industry_transitions": ["transition1"]
    }},
    "learning_resources": {{
        "courses": ["course1", "course2"],
        "books": ["book1", "book2"],
        "platforms": ["platform1", "platform2"]
    }},
    "milestones": [
        {{"milestone": "Milestone 1", "target_date": "2026-06"}},
        {{"milestone": "Milestone 2", "target_date": "2026-12"}}
    ]
}}
"""
            roadmap_text = self._generate_content(prompt)
            if not roadmap_text:
                return json.dumps({"error": "Unable to generate roadmap at this time"})
            
            # Extract JSON from the response
            try:
                json_str = extract_json_from_text(roadmap_text)
                json.loads(json_str)  # Validate it's valid JSON
                logger.info("Successfully generated career roadmap using Azure OpenAI")
                return json_str
            except:
                # If not JSON, return it as-is wrapped in JSON
                logger.info("Successfully generated career roadmap using Azure OpenAI (as text)")
                return json.dumps({"roadmap_text": roadmap_text})
            
        except Exception as e:
            logger.error(f"Error generating roadmap using Azure OpenAI: {e}")
            return json.dumps({"error": "Unable to generate roadmap at this time"})

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
            
            logger.info("Successfully extracted job requirements using Azure OpenAI")
            return result
            
        except Exception as e:
            logger.error(f"Error extracting job requirements using Azure OpenAI: {e}")
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
                
            logger.info("Successfully generated recommendations using Azure OpenAI")
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations using Azure OpenAI: {e}")
            return "Unable to generate recommendations at this time"

# Instance for easy import
AIEngine = AIEngine()
