"""Computes match scores between CV and job descriptions."""
import logging
from typing import List, Dict, Tuple
from utils.helpers import calculate_similarity

logger = logging.getLogger(__name__)


class JobMatcher:
    """Service for computing job-CV compatibility scores."""
    
    # Common skill categories
    TECHNICAL_SKILLS = {
        "python", "java", "javascript", "typescript", "sql", "react", "angular",
        "vue", "node", "django", "flask", "fastapi", "kubernetes", "docker",
        "aws", "azure", "gcp", "c++", "c#", ".net", "golang", "rust",
        "scala", "r", "matlab", "html", "css", "sass", "postgresql", "mongodb"
    }
    
    SOFT_SKILLS = {
        "leadership", "communication", "teamwork", "problem solving",
        "critical thinking", "creativity", "time management",
        "adaptability", "collaboration", "negotiation"
    }
    
    @staticmethod
    def compute_match_score(
        cv_skills: List[str],
        job_skills: List[str],
        cv_experience_years: int = 0,
        job_experience_required: int = 0
    ) -> int:
        """
        Compute match score between CV and job (0-100).
        
        Args:
            cv_skills: List of skills extracted from CV
            job_skills: List of required skills for job
            cv_experience_years: Years of experience from CV
            job_experience_required: Required years for job
            
        Returns:
            Match score 0-100
        """
        if not job_skills:
            return 0
        
        # Skill matching (60% weight)
        cv_skills_lower = {s.lower() for s in cv_skills}
        job_skills_lower = {s.lower() for s in job_skills}
        
        matched_skills = cv_skills_lower.intersection(job_skills_lower)
        skill_match_ratio = len(matched_skills) / len(job_skills_lower) if job_skills_lower else 0
        skill_score = min(int(skill_match_ratio * 100), 100)
        
        # Experience matching (25% weight)
        experience_score = 50  # Default
        if job_experience_required > 0 and cv_experience_years > 0:
            if cv_experience_years >= job_experience_required:
                experience_score = 100
            else:
                experience_score = int((cv_experience_years / job_experience_required) * 100)
        
        # Calculate weighted score
        total_score = int((skill_score * 0.6) + (experience_score * 0.25) + (50 * 0.15))
        
        return min(total_score, 100)
    
    @staticmethod
    def identify_missing_skills(
        cv_skills: List[str],
        job_skills: List[str]
    ) -> List[Dict[str, str]]:
        """
        Identify skills missing from CV that are required by job.
        
        Args:
            cv_skills: List of skills from CV
            job_skills: List of required skills
            
        Returns:
            List of missing skills with importance levels
        """
        cv_skills_lower = {s.lower() for s in cv_skills}
        missing = []
        
        for skill in job_skills:
            if skill.lower() not in cv_skills_lower:
                importance = JobMatcher._classify_skill_importance(skill)
                missing.append({
                    "skill": skill,
                    "importance": importance
                })
        
        # Sort by importance
        importance_order = {"high": 0, "medium": 1, "low": 2}
        missing.sort(key=lambda x: importance_order.get(x["importance"], 3))
        
        return missing
    
    @staticmethod
    def identify_strengths(cv_skills: List[str]) -> List[Dict[str, str]]:
        """
        Identify key strengths from CV skills.
        
        Args:
            cv_skills: List of skills from CV
            
        Returns:
            List of strengths with proficiency levels
        """
        strengths = []
        
        for skill in cv_skills:
            proficiency = JobMatcher._classify_proficiency(skill)
            strengths.append({
                "skill": skill,
                "proficiency": proficiency
            })
        
        # Sort by proficiency
        proficiency_order = {"expert": 0, "advanced": 1, "intermediate": 2, "beginner": 3}
        strengths.sort(key=lambda x: proficiency_order.get(x["proficiency"], 4))
        
        return strengths[:10]  # Return top 10 strengths
    
    @staticmethod
    def _classify_skill_importance(skill: str) -> str:
        """
        Classify skill importance level.
        
        Args:
            skill: Skill name
            
        Returns:
            Importance level: high, medium, or low
        """
        high_importance_keywords = {
            "python", "java", "javascript", "sql", "kubernetes", "docker",
            "aws", "azure", "machine learning", "leadership"
        }
        
        medium_importance_keywords = {
            "react", "node", "django", "git", "testing", "mongodb"
        }
        
        skill_lower = skill.lower()
        
        if any(keyword in skill_lower for keyword in high_importance_keywords):
            return "high"
        elif any(keyword in skill_lower for keyword in medium_importance_keywords):
            return "medium"
        else:
            return "low"
    
    @staticmethod
    def _classify_proficiency(skill: str) -> str:
        """
        Classify skill proficiency level based on keywords.
        
        Args:
            skill: Skill name
            
        Returns:
            Proficiency level: expert, advanced, intermediate, or beginner
        """
        skill_lower = skill.lower()
        
        expert_keywords = {"lead", "senior", "architect", "principal"}
        advanced_keywords = {"expert", "advanced", "proficient", "skilled"}
        intermediate_keywords = {"intermediate", "working knowledge"}
        
        if any(keyword in skill_lower for keyword in expert_keywords):
            return "expert"
        elif any(keyword in skill_lower for keyword in advanced_keywords):
            return "advanced"
        elif any(keyword in skill_lower for keyword in intermediate_keywords):
            return "intermediate"
        else:
            return "beginner"
    
    @staticmethod
    def rank_similar_jobs(
        cv_skills: List[str],
        job_list: List[Dict]
    ) -> List[Tuple[Dict, int]]:
        """
        Rank jobs by compatibility with CV skills.
        
        Args:
            cv_skills: Skills from CV
            job_list: List of job descriptions
            
        Returns:
            List of (job, match_score) tuples sorted by score
        """
        ranked_jobs = []
        
        for job in job_list:
            job_skills = job.get("skills", [])
            score = JobMatcher.compute_match_score(cv_skills, job_skills)
            ranked_jobs.append((job, score))
        
        # Sort by score descending
        ranked_jobs.sort(key=lambda x: x[1], reverse=True)
        
        return ranked_jobs