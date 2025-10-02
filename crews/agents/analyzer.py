# Analyzer Agent - Analyzes job compatibility and market trends

import json
import re
from datetime import datetime
from collections import Counter

class JobAnalyzer:
    def __init__(self, groq_api_key):
        self.groq_api_key = groq_api_key

    def analyze_job_compatibility(self, job_description, user_profile):
        """Analyze compatibility between job and user profile"""

        # Extract key information from job description
        job_requirements = self._extract_job_requirements(job_description)

        # Extract user skills and experience
        user_skills = user_profile.get("skills", [])
        user_experience = user_profile.get("experience_years", 0)
        user_education = user_profile.get("education", "")

        # Calculate compatibility scores
        skill_match_score = self._calculate_skill_match(job_requirements["skills"], user_skills)
        experience_match_score = self._calculate_experience_match(job_requirements["experience"], user_experience)
        education_match_score = self._calculate_education_match(job_requirements["education"], user_education)

        # Overall compatibility score (weighted average)
        overall_score = (
            skill_match_score * 0.5 +  # Skills are most important
            experience_match_score * 0.3 +  # Experience is important
            education_match_score * 0.2  # Education is least important
        )

        analysis = {
            "overall_score": round(overall_score, 1),
            "skill_match_score": round(skill_match_score, 1),
            "experience_match_score": round(experience_match_score, 1),
            "education_match_score": round(education_match_score, 1),
            "matching_skills": self._find_matching_skills(job_requirements["skills"], user_skills),
            "missing_skills": self._find_missing_skills(job_requirements["skills"], user_skills),
            "recommendations": self._generate_recommendations(job_requirements, user_profile),
            "analysis_date": datetime.now().isoformat()
        }

        return analysis

    def _extract_job_requirements(self, job_description):
        """Extract structured requirements from job description"""

        # Define skill keywords to look for
        technical_skills = [
            "python", "javascript", "java", "c++", "c#", "go", "rust", "php",
            "react", "angular", "vue", "node.js", "django", "flask", "fastapi",
            "sql", "postgresql", "mysql", "mongodb", "redis", "elasticsearch",
            "aws", "azure", "gcp", "docker", "kubernetes", "terraform",
            "git", "jenkins", "ci/cd", "agile", "scrum",
            "machine learning", "deep learning", "tensorflow", "pytorch", "scikit-learn",
            "pandas", "numpy", "matplotlib", "seaborn", "jupyter",
            "html", "css", "bootstrap", "tailwind", "sass",
            "rest api", "graphql", "microservices", "api design"
        ]

        # Extract skills mentioned in job description
        job_lower = job_description.lower()
        found_skills = []

        for skill in technical_skills:
            if skill in job_lower:
                found_skills.append(skill)

        # Extract experience requirements
        experience_years = self._extract_experience_years(job_description)

        # Extract education requirements
        education_level = self._extract_education_level(job_description)

        return {
            "skills": found_skills,
            "experience": experience_years,
            "education": education_level
        }

    def _extract_experience_years(self, job_description):
        """Extract required years of experience"""
        # Look for patterns like "2+ years", "3-5 years", etc.
        experience_patterns = [
            r"(\d+)\+?\s*years?",
            r"(\d+)-\d+\s*years?",
            r"minimum\s*(\d+)\s*years?",
            r"at least\s*(\d+)\s*years?"
        ]

        job_lower = job_description.lower()

        for pattern in experience_patterns:
            matches = re.findall(pattern, job_lower)
            if matches:
                return int(matches[0])

        # Default based on keywords
        if "senior" in job_lower or "lead" in job_lower:
            return 5
        elif "mid" in job_lower or "intermediate" in job_lower:
            return 3
        elif "entry" in job_lower or "junior" in job_lower:
            return 1
        else:
            return 2  # Default

    def _extract_education_level(self, job_description):
        """Extract education requirements"""
        job_lower = job_description.lower()

        if "phd" in job_lower or "doctorate" in job_lower:
            return "PhD"
        elif "master" in job_lower or "msc" in job_lower or "mba" in job_lower:
            return "Masters"
        elif "bachelor" in job_lower or "degree" in job_lower or "bsc" in job_lower:
            return "Bachelors"
        else:
            return "High School"

    def _calculate_skill_match(self, required_skills, user_skills):
        """Calculate skill match percentage"""
        if not required_skills:
            return 100  # No specific requirements

        user_skills_lower = [skill.lower() for skill in user_skills]
        matching_skills = [skill for skill in required_skills if skill.lower() in user_skills_lower]

        match_percentage = (len(matching_skills) / len(required_skills)) * 100
        return min(100, match_percentage)

    def _calculate_experience_match(self, required_years, user_years):
        """Calculate experience match score"""
        if user_years >= required_years:
            return 100
        elif user_years >= required_years * 0.7:  # Within 30% of requirement
            return 80
        elif user_years >= required_years * 0.5:  # Within 50% of requirement
            return 60
        else:
            return 40

    def _calculate_education_match(self, required_education, user_education):
        """Calculate education match score"""
        education_levels = {
            "High School": 1,
            "Bachelors": 2,
            "Masters": 3,
            "PhD": 4
        }

        required_level = education_levels.get(required_education, 2)
        user_level = education_levels.get(user_education, 2)

        if user_level >= required_level:
            return 100
        elif user_level == required_level - 1:
            return 80
        else:
            return 60

    def _find_matching_skills(self, required_skills, user_skills):
        """Find skills that match between requirements and user profile"""
        user_skills_lower = [skill.lower() for skill in user_skills]
        return [skill for skill in required_skills if skill.lower() in user_skills_lower]

    def _find_missing_skills(self, required_skills, user_skills):
        """Find skills that are required but missing from user profile"""
        user_skills_lower = [skill.lower() for skill in user_skills]
        return [skill for skill in required_skills if skill.lower() not in user_skills_lower]

    def _generate_recommendations(self, job_requirements, user_profile):
        """Generate recommendations for improving job compatibility"""
        recommendations = []

        missing_skills = self._find_missing_skills(job_requirements["skills"], user_profile.get("skills", []))

        if missing_skills:
            recommendations.append({
                "type": "skill_development",
                "message": f"Consider learning these skills: {', '.join(missing_skills[:3])}",
                "priority": "high" if len(missing_skills) > 3 else "medium"
            })

        required_experience = job_requirements["experience"]
        user_experience = user_profile.get("experience_years", 0)

        if user_experience < required_experience:
            recommendations.append({
                "type": "experience",
                "message": f"Gain {required_experience - user_experience} more years of experience",
                "priority": "medium"
            })

        if len(missing_skills) <= 2 and user_experience >= required_experience * 0.8:
            recommendations.append({
                "type": "application",
                "message": "You're a strong candidate! Consider applying.",
                "priority": "high"
            })

        return recommendations

    def analyze_market_trends(self, job_listings):
        """Analyze trends across multiple job listings"""
        all_skills = []
        all_companies = []
        salary_ranges = []

        for job in job_listings:
            # Extract skills from each job
            job_requirements = self._extract_job_requirements(job.get("description", ""))
            all_skills.extend(job_requirements["skills"])

            # Collect company info
            if "company" in job:
                all_companies.append(job["company"])

            # Collect salary info if available
            if "salary_range" in job:
                salary_ranges.append(job["salary_range"])

        # Analyze trends
        skill_frequency = Counter(all_skills)
        company_frequency = Counter(all_companies)

        trends = {
            "most_demanded_skills": skill_frequency.most_common(10),
            "top_hiring_companies": company_frequency.most_common(10),
            "total_jobs_analyzed": len(job_listings),
            "analysis_date": datetime.now().isoformat()
        }

        return trends