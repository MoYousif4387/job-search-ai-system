# Job Scout Agent - Finds relevant job opportunities

import requests
import json
from datetime import datetime

class JobScout:
    def __init__(self, groq_api_key):
        self.groq_api_key = groq_api_key

    def search_jobs(self, keywords, location="remote"):
        """Search for jobs using multiple job board APIs"""
        jobs = []

        # Example: Using a hypothetical job API
        # In real implementation, you'd use actual job board APIs like:
        # - Indeed API
        # - LinkedIn API
        # - GitHub Jobs API
        # - Stack Overflow Jobs API

        # Simulated job data for demonstration
        simulated_jobs = [
            {
                "title": "Python Developer",
                "company": "TechCorp Inc",
                "location": "London, ON",
                "description": "Looking for a Python developer with experience in Django, FastAPI, and machine learning. Must have 2+ years experience.",
                "url": "https://example.com/job1",
                "posted_date": datetime.now().isoformat(),
                "salary_range": "70000-90000"
            },
            {
                "title": "Full Stack Developer",
                "company": "StartupXYZ",
                "location": "Remote",
                "description": "Seeking full stack developer proficient in React, Node.js, and Python. Experience with AWS preferred.",
                "url": "https://example.com/job2",
                "posted_date": datetime.now().isoformat(),
                "salary_range": "60000-80000"
            },
            {
                "title": "AI/ML Engineer",
                "company": "DataCorp",
                "location": "Toronto, ON",
                "description": "AI/ML Engineer role requiring Python, TensorFlow, PyTorch experience. PhD preferred but not required.",
                "url": "https://example.com/job3",
                "posted_date": datetime.now().isoformat(),
                "salary_range": "90000-120000"
            }
        ]

        # Filter jobs based on keywords
        filtered_jobs = []
        keywords_lower = [k.lower() for k in keywords]

        for job in simulated_jobs:
            job_text = f"{job['title']} {job['description']}".lower()
            if any(keyword in job_text for keyword in keywords_lower):
                filtered_jobs.append(job)

        return filtered_jobs

    def score_job_relevance(self, job, user_skills):
        """Score how relevant a job is based on user skills"""
        description = job['description'].lower()
        title = job['title'].lower()

        score = 0
        max_score = len(user_skills) * 10

        for skill in user_skills:
            skill_lower = skill.lower()
            if skill_lower in description:
                score += 10
            elif skill_lower in title:
                score += 8

        # Normalize to 0-100 scale
        relevance_score = min(100, (score / max_score) * 100) if max_score > 0 else 0

        return {
            **job,
            "relevance_score": relevance_score,
            "matching_skills": [skill for skill in user_skills if skill.lower() in description.lower()]
        }