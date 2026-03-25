"""Generates career improvement plans based on analysis."""
import logging
from typing import List, Dict, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class RoadmapGenerator:
    """Service for generating structured career development roadmaps."""
    
    @staticmethod
    def generate_learning_roadmap(
        missing_skills: List[Dict[str, str]],
        target_role: Optional[str] = None,
        timeline_months: int = 12
    ) -> str:
        """
        Generate structured learning roadmap for missing skills.
        
        Args:
            missing_skills: List of missing skills with importance
            target_role: Optional target role
            timeline_months: Total timeline in months
            
        Returns:
            Structured roadmap as formatted text
        """
        roadmap = []
        roadmap.append("=" * 60)
        roadmap.append("CAREER DEVELOPMENT ROADMAP")
        roadmap.append("=" * 60)
        
        if target_role:
            roadmap.append(f"\nTarget Role: {target_role}")
        
        roadmap.append(f"Timeline: {timeline_months} months")
        roadmap.append(f"Generated: {datetime.utcnow().strftime('%Y-%m-%d')}")
        roadmap.append("")
        
        # Phase breakdown
        phase_duration = timeline_months // 3
        if phase_duration == 0:
            phase_duration = 1
        
        phases = [
            ("Phase 1: Foundation", 0, phase_duration),
            ("Phase 2: Development", phase_duration, phase_duration * 2),
            ("Phase 3: Mastery", phase_duration * 2, timeline_months)
        ]
        
        # Categorize skills by importance
        high_priority = [s for s in missing_skills if s.get("importance") == "high"]
        medium_priority = [s for s in missing_skills if s.get("importance") == "medium"]
        low_priority = [s for s in missing_skills if s.get("importance") == "low"]
        
        # Phase 1: Foundation
        roadmap.append("\n" + phases[0][0])
        roadmap.append("-" * 60)
        roadmap.append(f"Duration: Months 1-{phase_duration}")
        roadmap.append("Focus: Building foundational knowledge")
        roadmap.append("\nKey Skills to Learn:")
        for i, skill in enumerate(high_priority[:3], 1):
            roadmap.append(f"  {i}. {skill['skill']} (High Priority)")
        roadmap.append("\nActions:")
        roadmap.append("  • Enroll in foundational courses")
        roadmap.append("  • Complete 2-3 online certifications")
        roadmap.append("  • Start a small project to apply learning")
        roadmap.append("  • Join relevant communities/forums")
        roadmap.append("  • Read industry blogs and documentation")
        
        # Phase 2: Development
        roadmap.append("\n" + phases[1][0])
        roadmap.append("-" * 60)
        roadmap.append(f"Duration: Months {phase_duration + 1}-{phase_duration * 2}")
        roadmap.append("Focus: Deepening expertise and practical application")
        roadmap.append("\nKey Skills to Learn:")
        for i, skill in enumerate(medium_priority[:3], 1):
            roadmap.append(f"  {i}. {skill['skill']} (Medium Priority)")
        roadmap.append("\nActions:")
        roadmap.append("  • Build 2-3 real-world projects")
        roadmap.append("  • Contribute to open source")
        roadmap.append("  • Attend workshops and meetups")
        roadmap.append("  • Seek mentorship from experts")
        roadmap.append("  • Write technical blog posts")
        
        # Phase 3: Mastery
        roadmap.append("\n" + phases[2][0])
        roadmap.append("-" * 60)
        roadmap.append(f"Duration: Months {phase_duration * 2 + 1}-{timeline_months}")
        roadmap.append("Focus: Mastery and thought leadership")
        roadmap.append("\nKey Skills to Learn:")
        for i, skill in enumerate(low_priority[:3], 1):
            roadmap.append(f"  {i}. {skill['skill']} (Supporting Skills)")
        roadmap.append("\nActions:")
        roadmap.append("  • Lead projects or initiatives")
        roadmap.append("  • Create course or training material")
        roadmap.append("  • Build impressive portfolio")
        roadmap.append("  • Network with industry leaders")
        roadmap.append("  • Prepare for target role interviews")
        
        # Learning resources
        roadmap.append("\n" + "=" * 60)
        roadmap.append("RECOMMENDED LEARNING RESOURCES")
        roadmap.append("=" * 60)
        roadmap.append("\nOnline Platforms:")
        roadmap.append("  • Coursera - Industry-recognized courses")
        roadmap.append("  • Udemy - Practical, affordable courses")
        roadmap.append("  • LinkedIn Learning - Professional development")
        roadmap.append("  • Pluralsight - Tech-focused training")
        roadmap.append("  • FreeCodeCamp - Free coding resources")
        
        roadmap.append("\nCommunities:")
        roadmap.append("  • GitHub - Open source contribution")
        roadmap.append("  • Stack Overflow - Q&A and learning")
        roadmap.append("  • Dev.to - Tech blogging community")
        roadmap.append("  • HackerRank - Coding challenges")
        roadmap.append("  • Kaggle - Data science competitions")
        
        # Milestones
        roadmap.append("\n" + "=" * 60)
        roadmap.append("KEY MILESTONES")
        roadmap.append("=" * 60)
        
        milestones = [
            (phase_duration, "Complete foundational certifications"),
            (phase_duration * 2, "Deploy first major project"),
            (timeline_months, "Achieve target role readiness")
        ]
        
        for month, milestone in milestones:
            roadmap.append(f"  Month {month}: {milestone}")
        
        roadmap.append("\n" + "=" * 60)
        
        return "\n".join(roadmap)
    
    @staticmethod
    def generate_skill_progression(
        current_skills: List[str],
        target_skills: List[str],
        timeline_weeks: int = 52
    ) -> Dict:
        """
        Generate detailed skill progression plan.
        
        Args:
            current_skills: Current skills
            target_skills: Target skills to acquire
            timeline_weeks: Timeline in weeks
            
        Returns:
            Dictionary with progression plan
        """
        return {
            "current_skills_count": len(current_skills),
            "target_skills_count": len(target_skills),
            "skills_to_develop": len(set(target_skills) - set(current_skills)),
            "weekly_commitment_hours": RoadmapGenerator._calculate_commitment(
                len(set(target_skills) - set(current_skills)),
                timeline_weeks
            ),
            "estimated_completion_date": (
                datetime.utcnow() + timedelta(weeks=timeline_weeks)
            ).strftime("%Y-%m-%d"),
            "difficulty_level": RoadmapGenerator._assess_difficulty(
                len(set(target_skills) - set(current_skills))
            )
        }
    
    @staticmethod
    def _calculate_commitment(skills_to_develop: int, weeks: int) -> int:
        """Calculate recommended weekly study hours."""
        base_hours = 10  # Base 10 hours per week
        hours_per_skill = 15  # 15 hours per new skill
        total_hours = hours_per_skill * skills_to_develop
        return max(int(total_hours / weeks), base_hours)
    
    @staticmethod
    def _assess_difficulty(skills_count: int) -> str:
        """Assess overall difficulty based on skills to learn."""
        if skills_count <= 2:
            return "Easy"
        elif skills_count <= 5:
            return "Moderate"
        elif skills_count <= 10:
            return "Challenging"
        else:
            return "Very Challenging"
    
    @staticmethod
    def generate_interview_prep_plan(
        target_role: str,
        missing_skills: List[Dict[str, str]]
    ) -> str:
        """
        Generate interview preparation plan.
        
        Args:
            target_role: Target role name
            missing_skills: List of missing skills
            
        Returns:
            Interview prep plan text
        """
        plan = []
        plan.append("=" * 60)
        plan.append(f"INTERVIEW PREPARATION FOR {target_role.upper()}")
        plan.append("=" * 60)
        
        plan.append("\n1. TECHNICAL PREPARATION")
        plan.append("-" * 60)
        plan.append("  • Review core concepts related to the role")
        plan.append("  • Practice coding/technical problems")
        plan.append("  • Prepare project demonstrations")
        plan.append("  • Study industry best practices")
        
        plan.append("\n2. BEHAVIORAL PREPARATION")
        plan.append("-" * 60)
        plan.append("  • Prepare STAR method examples")
        plan.append("  • Research the company thoroughly")
        plan.append("  • Prepare questions to ask interviewers")
        plan.append("  • Practice mock interviews")
        
        plan.append("\n3. SKILLS TO HIGHLIGHT")
        plan.append("-" * 60)
        high_priority = [s for s in missing_skills if s.get("importance") == "high"]
        for skill in high_priority[:5]:
            plan.append(f"  • {skill['skill']}: Prepare examples and projects")
        
        plan.append("\n4. TIMELINE (2 WEEKS BEFORE INTERVIEW)")
        plan.append("-" * 60)
        plan.append("  Week 1:")
        plan.append("    • Day 1-2: Deep dive into technical requirements")
        plan.append("    • Day 3-4: Complete practice problems")
        plan.append("    • Day 5-7: Company research and mock interviews")
        plan.append("  Week 2:")
        plan.append("    • Day 1-3: Review weak areas")
        plan.append("    • Day 4-5: Final practice and polish")
        plan.append("    • Day 6-7: Rest and final preparation")
        
        plan.append("\n" + "=" * 60)
        
        return "\n".join(plan)