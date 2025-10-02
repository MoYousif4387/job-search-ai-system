#!/usr/bin/env python3
"""
Simple FastAPI service for job processing without CrewAI dependencies
This provides basic functionality while CrewAI installs
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
from job_sources import JobBoardIntegrator

app = FastAPI(title="CP494 Job Application API (Simple)", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize job board integrator
job_integrator = JobBoardIntegrator()

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

# Sample job data focused on internships and new grad opportunities
SAMPLE_JOBS = [
    {
        "title": "Software Engineering Intern - Summer 2025",
        "company": "Shopify",
        "location": "Toronto, ON",
        "description": "Looking for computer science students for summer 2025 internship. Experience with Python, JavaScript, or Java preferred. No prior professional experience required. Will work on real products used by millions of merchants.",
        "url": "https://example.com/intern1",
        "posted_date": "2025-01-01",
        "salary_range": "5000-7000/month",
        "relevance_score": 92
    },
    {
        "title": "New Graduate Software Developer",
        "company": "RBC",
        "location": "Toronto, ON",
        "description": "Entry-level position for recent Computer Science graduates. Join our technology graduate program. Training provided. Looking for knowledge in Python, Java, or C++. Recent graduates welcome.",
        "url": "https://example.com/newgrad1",
        "posted_date": "2025-01-01",
        "salary_range": "65000-75000",
        "relevance_score": 89
    },
    {
        "title": "Data Engineering Intern",
        "company": "TD Bank",
        "location": "Toronto, ON",
        "description": "Summer internship opportunity for students studying Computer Science, Data Science, or related fields. Experience with Python, SQL, and data processing frameworks preferred but not required.",
        "url": "https://example.com/intern2",
        "posted_date": "2025-01-01",
        "salary_range": "4500-6000/month",
        "relevance_score": 88
    },
    {
        "title": "Junior Python Developer (New Grad)",
        "company": "Wealthsimple",
        "location": "Toronto, ON",
        "description": "Entry-level Python developer position for recent graduates. Will work on fintech applications. Looking for new grads with Python knowledge and eagerness to learn. Mentorship provided.",
        "url": "https://example.com/newgrad2",
        "posted_date": "2025-01-01",
        "salary_range": "70000-80000",
        "relevance_score": 91
    },
    {
        "title": "Software Engineering Co-op",
        "company": "Blackberry",
        "location": "Waterloo, ON",
        "description": "4-month co-op position for computer science students. Experience with C++, Python, or Java. Will work on cybersecurity and IoT products. Previous co-op experience an asset but not required.",
        "url": "https://example.com/coop1",
        "posted_date": "2025-01-01",
        "salary_range": "4800-6200/month",
        "relevance_score": 87
    },
    {
        "title": "Machine Learning Intern",
        "company": "Vector Institute",
        "location": "Toronto, ON",
        "description": "Research internship for students interested in AI/ML. Experience with Python, TensorFlow/PyTorch preferred. Will work alongside researchers on cutting-edge AI projects. Academic credit available.",
        "url": "https://example.com/intern3",
        "posted_date": "2025-01-01",
        "salary_range": "5500-7500/month",
        "relevance_score": 94
    }
]

# Database helper
def get_db_connection():
    """Get database connection"""
    db_path = "database/applications.db"
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    return sqlite3.connect(db_path)

def init_database():
    """Initialize database with schema"""
    conn = get_db_connection()
    cursor = conn.cursor()

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

    conn.commit()
    conn.close()

@app.get("/")
async def root():
    return {"message": "CP494 Job Application API (Simple) is running!"}

@app.post("/search-jobs")
async def search_jobs(request: JobSearchRequest):
    """Search for jobs using real job sources with sample data fallback"""
    try:
        # Try to get real jobs first
        try:
            print(f"Searching real job sources for: {request.keywords}")
            real_jobs = job_integrator.search_all_sources(
                keywords=request.keywords,
                location=request.location,
                limit_per_source=3
            )

            if real_jobs:
                print(f"Found {len(real_jobs)} real jobs")
                return {
                    "jobs": real_jobs[:request.limit],
                    "total_found": len(real_jobs),
                    "search_params": {
                        "keywords": request.keywords,
                        "location": request.location
                    },
                    "data_source": "Real job boards (Indeed, LinkedIn, Government, Universities)"
                }
        except Exception as e:
            print(f"Real job search failed: {e}, falling back to sample data")

        # Fallback to sample data
        print("Using sample job data")
        keywords_list = [k.strip().lower() for k in request.keywords.split(",")]

        # Filter jobs based on keywords
        matching_jobs = []
        for job in SAMPLE_JOBS:
            job_text = f"{job['title']} {job['description']}".lower()

            # Check if any keyword matches
            if any(keyword in job_text for keyword in keywords_list):
                matching_jobs.append(job)

        # Sort by relevance score
        matching_jobs.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)

        return {
            "jobs": matching_jobs[:request.limit],
            "total_found": len(matching_jobs),
            "search_params": {
                "keywords": request.keywords,
                "location": request.location
            },
            "data_source": "Sample data (real integration available)"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job search failed: {str(e)}")

@app.post("/analyze-job")
async def analyze_job(request: JobAnalysisRequest):
    """Analyze job compatibility using simple matching"""
    try:
        # Simple compatibility analysis
        user_skills_lower = [skill.strip().lower() for skill in request.user_skills]

        # Sample job requirements based on the GTS job description
        job_requirements = [
            "python", "mysql", "linux", "fastapi", "airflow",
            "kafka", "redis", "docker", "api development"
        ]

        # Calculate matches
        matching_skills = [skill for skill in job_requirements if skill in user_skills_lower]
        missing_skills = [skill for skill in job_requirements if skill not in user_skills_lower]

        # Calculate scores
        skill_match_score = (len(matching_skills) / len(job_requirements)) * 100
        overall_score = min(95, skill_match_score + 20)  # Bonus for experience

        analysis = {
            "overall_score": round(overall_score, 1),
            "skill_match_score": round(skill_match_score, 1),
            "experience_match_score": 85.0,  # Assuming good experience match
            "education_match_score": 90.0,   # Assuming good education match
            "matching_skills": matching_skills,
            "missing_skills": missing_skills,
            "recommendations": [
                {
                    "type": "skill_development",
                    "message": f"Consider learning: {', '.join(missing_skills[:3])}",
                    "priority": "medium"
                },
                {
                    "type": "application",
                    "message": "Strong candidate - consider applying!",
                    "priority": "high"
                }
            ]
        }

        return {
            "analysis": analysis,
            "job_url": request.job_url,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job analysis failed: {str(e)}")

@app.post("/generate-resume")
async def generate_resume(request: ResumeRequest):
    """Generate tailored resume using simple template"""
    try:
        # Extract key skills from job description
        job_desc_lower = request.job_description.lower()
        important_skills = []

        skill_keywords = [
            "python", "javascript", "java", "sql", "aws", "docker",
            "kubernetes", "react", "node.js", "fastapi", "django",
            "machine learning", "tensorflow", "pytorch", "linux",
            "mysql", "postgresql", "redis", "kafka", "airflow"
        ]

        for skill in skill_keywords:
            if skill in job_desc_lower:
                important_skills.append(skill.title())

        # Create tailored resume
        tailored_resume = {
            "summary": f"Experienced software developer with expertise in {', '.join(important_skills[:5])}. Proven track record in building scalable systems and collaborating with cross-functional teams.",
            "skills": important_skills,
            "experience": [
                {
                    "title": "Advanced Analytics & BI Intern",
                    "company": "Sun Life",
                    "description": f"Built end-to-end systems using {', '.join(important_skills[:3])}, serving 290+ users with optimized performance."
                },
                {
                    "title": "Data Engineering Intern",
                    "company": "CIBC",
                    "description": f"Contributed to large-scale distributed systems, worked with {', '.join(important_skills[1:4])} for financial data processing."
                }
            ],
            "tailored_for": {
                "job_title": "Software Developer",
                "company": "Target Company",
                "date_created": datetime.now().isoformat()
            }
        }

        # Generate cover letter
        cover_letter = f"""
Dear Hiring Manager,

I am writing to express my strong interest in the Software Developer position.
With my background in {', '.join(important_skills[:3])}, I am confident I would be
a valuable addition to your team.

My experience with {', '.join(important_skills[:5])} aligns perfectly with your
requirements. I am particularly excited about the opportunity to contribute to
your innovative environment.

Best regards,
Mahmoud Yousif
        """.strip()

        return {
            "tailored_resume": tailored_resume,
            "cover_letter": cover_letter,
            "job_requirements": important_skills,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Resume generation failed: {str(e)}")

@app.post("/save-application")
async def save_application(application_data: Dict[str, Any]):
    """Save job application to database"""
    try:
        init_database()  # Ensure database exists
        conn = get_db_connection()
        cursor = conn.cursor()

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
        init_database()  # Ensure database exists
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
            "database": "available",
            "job_search": "active",
            "resume_generator": "active"
        }
    }

if __name__ == "__main__":
    import uvicorn
    print("Starting Simple Job Application API...")
    print("Visit http://localhost:8000 for the API")
    print("Visit http://localhost:8000/docs for interactive documentation")
    uvicorn.run(app, host="0.0.0.0", port=8000)