#!/usr/bin/env python3
"""
FastAPI service for CrewAI agents and job processing
This service provides the AI functionality for the job application system
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import json
import sqlite3
from datetime import datetime
from typing import List, Dict, Any
import requests
from groq import Groq

# Import our CrewAI agents
from crews.job_application_crew import JobApplicationSystem
from crews.agents.job_scout import JobScout
from crews.agents.resume_writer import ResumeWriter
from crews.agents.analyzer import JobAnalyzer

app = FastAPI(title="CP494 Job Application API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
groq_api_key = os.getenv("GROQ_API_KEY")
job_system = JobApplicationSystem()
job_scout = JobScout(groq_api_key)
resume_writer = ResumeWriter(groq_api_key)
job_analyzer = JobAnalyzer(groq_api_key)

# Pydantic models
class JobSearchRequest(BaseModel):
    keywords: str
    location: str = "remote"
    limit: int = 10

class JobAnalysisRequest(BaseModel):
    job_url: str
    user_skills: List[str]

class ResumeRequest(BaseModel):
    job_description: str
    base_resume: str

class UserProfile(BaseModel):
    skills: List[str]
    experience_years: int
    education: str

# Database helper
def get_db_connection():
    """Get database connection"""
    db_path = "database/applications.db"
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    return sqlite3.connect(db_path)

@app.get("/")
async def root():
    return {"message": "CP494 Job Application API is running!"}

@app.post("/search-jobs")
async def search_jobs(request: JobSearchRequest):
    """Search for jobs using our job scout agent"""
    try:
        # Use our job scout to find jobs
        jobs = job_scout.search_jobs(
            keywords=request.keywords.split(","),
            location=request.location
        )

        # Score each job for relevance
        user_skills = ["python", "javascript", "sql", "aws", "docker"]  # Default skills
        scored_jobs = []

        for job in jobs:
            scored_job = job_scout.score_job_relevance(job, user_skills)
            scored_jobs.append(scored_job)

        # Sort by relevance score
        scored_jobs.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)

        return {
            "jobs": scored_jobs[:request.limit],
            "total_found": len(scored_jobs),
            "search_params": {
                "keywords": request.keywords,
                "location": request.location
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job search failed: {str(e)}")

@app.post("/analyze-job")
async def analyze_job(request: JobAnalysisRequest):
    """Analyze job compatibility using our analyzer agent"""
    try:
        # Create user profile from skills
        user_profile = {
            "skills": request.user_skills,
            "experience_years": 3,  # Default
            "education": "Bachelors"  # Default
        }

        # For demo, we'll use a sample job description
        # In production, you'd fetch the actual job from the URL
        sample_job_description = """
        We are looking for a Python developer with experience in:
        - Python programming (3+ years)
        - FastAPI or Django
        - SQL databases
        - AWS cloud services
        - Docker containerization

        Requirements:
        - Bachelor's degree in Computer Science
        - Strong problem-solving skills
        - Experience with REST APIs
        """

        # Analyze compatibility
        analysis = job_analyzer.analyze_job_compatibility(
            sample_job_description,
            user_profile
        )

        return {
            "analysis": analysis,
            "job_url": request.job_url,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job analysis failed: {str(e)}")

@app.post("/generate-resume")
async def generate_resume(request: ResumeRequest):
    """Generate tailored resume using our resume writer agent"""
    try:
        # Extract job requirements
        job_requirements = resume_writer.analyze_job_requirements(request.job_description)

        # Create tailored resume
        tailored_resume = resume_writer.tailor_resume(
            base_resume=request.base_resume,
            job_requirements=job_requirements,
            job_title="Software Developer",  # Extract from job description
            company_name="Target Company"    # Extract from job description
        )

        # Generate cover letter
        cover_letter = resume_writer.generate_cover_letter(
            job_title="Software Developer",
            company_name="Target Company",
            job_requirements=job_requirements,
            user_background=request.base_resume
        )

        return {
            "tailored_resume": tailored_resume,
            "cover_letter": cover_letter,
            "job_requirements": job_requirements,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Resume generation failed: {str(e)}")

@app.post("/save-application")
async def save_application(application_data: Dict[str, Any]):
    """Save job application to database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Create table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY,
                job_title TEXT,
                company TEXT,
                job_url TEXT,
                compatibility_score REAL,
                date_found DATE,
                date_applied DATE,
                status TEXT
            )
        """)

        # Insert application
        cursor.execute("""
            INSERT INTO applications
            (job_title, company, job_url, compatibility_score, date_found, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            application_data.get("job_title"),
            application_data.get("company"),
            application_data.get("job_url"),
            application_data.get("compatibility_score", 0),
            datetime.now().date(),
            "found"
        ))

        conn.commit()
        application_id = cursor.lastrowid
        conn.close()

        return {
            "message": "Application saved successfully",
            "application_id": application_id
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save application: {str(e)}")

@app.get("/applications")
async def get_applications():
    """Get all job applications from database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, job_title, company, compatibility_score,
                   date_found, status
            FROM applications
            ORDER BY date_found DESC
        """)

        results = cursor.fetchall()
        conn.close()

        applications = []
        for row in results:
            applications.append({
                "id": row[0],
                "job_title": row[1],
                "company": row[2],
                "compatibility_score": row[3],
                "date_found": row[4],
                "status": row[5]
            })

        return {"applications": applications}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch applications: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "groq_api": "configured" if groq_api_key else "missing",
            "database": "available",
            "ai_agents": "loaded"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)