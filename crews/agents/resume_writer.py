# Resume Writer Agent - Creates tailored resumes

import json
from datetime import datetime

class ResumeWriter:
    def __init__(self, groq_api_key):
        self.groq_api_key = groq_api_key

    def analyze_job_requirements(self, job_description):
        """Extract key requirements from job description"""
        # In a real implementation, this would use NLP to extract requirements
        # For now, we'll use keyword matching

        technical_skills = [
            "python", "javascript", "react", "node.js", "django", "fastapi",
            "sql", "mongodb", "aws", "docker", "kubernetes", "git",
            "machine learning", "tensorflow", "pytorch", "pandas", "numpy"
        ]

        soft_skills = [
            "teamwork", "communication", "leadership", "problem solving",
            "analytical", "detail-oriented", "self-motivated", "collaborative"
        ]

        found_technical = []
        found_soft = []

        job_lower = job_description.lower()

        for skill in technical_skills:
            if skill in job_lower:
                found_technical.append(skill)

        for skill in soft_skills:
            if skill in job_lower:
                found_soft.append(skill)

        return {
            "technical_skills": found_technical,
            "soft_skills": found_soft,
            "experience_level": self._extract_experience_level(job_description),
            "education_requirements": self._extract_education_requirements(job_description)
        }

    def _extract_experience_level(self, job_description):
        """Extract required experience level"""
        job_lower = job_description.lower()

        if "entry level" in job_lower or "0-1 years" in job_lower:
            return "entry"
        elif "2-3 years" in job_lower or "mid level" in job_lower:
            return "mid"
        elif "senior" in job_lower or "5+ years" in job_lower:
            return "senior"
        else:
            return "mid"  # Default

    def _extract_education_requirements(self, job_description):
        """Extract education requirements"""
        job_lower = job_description.lower()

        if "phd" in job_lower or "doctorate" in job_lower:
            return "PhD"
        elif "master" in job_lower or "msc" in job_lower:
            return "Masters"
        elif "bachelor" in job_lower or "degree" in job_lower:
            return "Bachelors"
        else:
            return "Bachelors"  # Default

    def tailor_resume(self, base_resume, job_requirements, job_title, company_name):
        """Create a tailored resume based on job requirements"""

        # Parse the base resume (assuming it's a JSON structure)
        if isinstance(base_resume, str):
            try:
                resume_data = json.loads(base_resume)
            except:
                # If it's not JSON, create a basic structure
                resume_data = {
                    "summary": base_resume[:200] + "..." if len(base_resume) > 200 else base_resume,
                    "skills": [],
                    "experience": [],
                    "education": []
                }
        else:
            resume_data = base_resume

        # Tailor the resume
        tailored_resume = {
            "summary": self._tailor_summary(resume_data.get("summary", ""), job_requirements, job_title),
            "skills": self._highlight_relevant_skills(resume_data.get("skills", []), job_requirements),
            "experience": self._tailor_experience(resume_data.get("experience", []), job_requirements),
            "education": resume_data.get("education", []),
            "tailored_for": {
                "job_title": job_title,
                "company": company_name,
                "date_created": datetime.now().isoformat()
            }
        }

        return tailored_resume

    def _tailor_summary(self, original_summary, job_requirements, job_title):
        """Create a tailored professional summary"""
        technical_skills = job_requirements.get("technical_skills", [])

        # Create a summary that emphasizes relevant skills
        if technical_skills:
            skills_text = ", ".join(technical_skills[:5])  # Top 5 skills
            tailored = f"Experienced professional specializing in {skills_text}. "
            tailored += f"Passionate about {job_title.lower()} role with proven expertise in "
            tailored += f"{', '.join(technical_skills[:3])}. "
            tailored += original_summary
        else:
            tailored = original_summary

        return tailored

    def _highlight_relevant_skills(self, original_skills, job_requirements):
        """Reorder and highlight skills relevant to the job"""
        technical_skills = job_requirements.get("technical_skills", [])

        # Put relevant skills first
        relevant_skills = []
        other_skills = []

        for skill in original_skills:
            if skill.lower() in [req.lower() for req in technical_skills]:
                relevant_skills.append(skill)
            else:
                other_skills.append(skill)

        # Add any required skills that might be missing (if user has them)
        for req_skill in technical_skills:
            if req_skill not in [skill.lower() for skill in relevant_skills]:
                relevant_skills.append(req_skill.title())

        return relevant_skills + other_skills

    def _tailor_experience(self, original_experience, job_requirements):
        """Tailor experience descriptions to highlight relevant aspects"""
        technical_skills = job_requirements.get("technical_skills", [])

        tailored_experience = []

        for exp in original_experience:
            tailored_exp = exp.copy()

            # Enhance descriptions with relevant keywords
            if "description" in exp:
                description = exp["description"]
                for skill in technical_skills:
                    if skill.lower() in description.lower():
                        # Highlight this skill in the description
                        description = description.replace(
                            skill.lower(),
                            f"**{skill}**"
                        )
                tailored_exp["description"] = description

            tailored_experience.append(tailored_exp)

        return tailored_experience

    def generate_cover_letter(self, job_title, company_name, job_requirements, user_background):
        """Generate a tailored cover letter"""
        technical_skills = job_requirements.get("technical_skills", [])

        cover_letter = f"""
Dear Hiring Manager,

I am writing to express my strong interest in the {job_title} position at {company_name}.
With my background in {', '.join(technical_skills[:3])}, I am confident that I would be
a valuable addition to your team.

My experience with {', '.join(technical_skills[:5])} aligns perfectly with your
requirements. I am particularly excited about the opportunity to contribute to
{company_name}'s mission and grow within your innovative environment.

I have attached my resume for your review and would welcome the opportunity to
discuss how my skills and enthusiasm can benefit your team.

Thank you for your consideration.

Best regards,
[Your Name]
        """

        return cover_letter.strip()