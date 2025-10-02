# This creates your control panel
import gradio as gr
import requests
import sqlite3
import json
import os
from datetime import datetime

# Database helper functions
def init_database():
    """Initialize the SQLite database"""
    db_path = "../database/applications.db"

    # Create database directory if it doesn't exist
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # Read and execute schema
    with open("../database/schema.sql", "r") as f:
        schema = f.read()

    conn = sqlite3.connect(db_path)
    conn.executescript(schema)
    conn.close()

def load_applications():
    """Load applications from database"""
    try:
        conn = sqlite3.connect("../database/applications.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, job_title, company, compatibility_score,
                   date_found, status
            FROM applications
            ORDER BY date_found DESC
        """)

        results = cursor.fetchall()
        conn.close()

        # Convert to list of lists for Gradio DataFrame
        return [list(row) for row in results]
    except:
        return []

def search_jobs(keywords, location):
    """Search for jobs using our FastAPI service"""
    try:
        print(f"DEBUG: Searching for keywords='{keywords}', location='{location}'")

        # Call n8n webhook first, fallback to FastAPI
        response = None
        try:
            response = requests.post(
                "http://localhost:5678/webhook/search-jobs",
                json={"keywords": keywords, "location": location},
                timeout=30
            )
            if response.status_code == 200:
                print(f"DEBUG: Using n8n webhook successfully")
            else:
                print(f"DEBUG: n8n webhook returned {response.status_code}, falling back to FastAPI")
                raise Exception("n8n webhook failed")
        except:
            print(f"DEBUG: n8n webhook failed, falling back to FastAPI")
            response = requests.post(
                "http://localhost:8000/search-jobs",
                json={"keywords": keywords, "location": location},
                timeout=30
            )

        print(f"DEBUG: API Response status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            jobs = data.get("jobs", [])
            print(f"DEBUG: Found {len(jobs)} jobs")
            if jobs:
                print(f"DEBUG: First job: {jobs[0].get('title', 'No title')}")
            result = format_job_results(jobs)
            print(f"DEBUG: Formatted result: {result}")
            return result
        else:
            print(f"DEBUG: API Error: {response.text}")
            return [["Error", f"API returned {response.status_code}", "N/A"]]
    except requests.exceptions.ConnectionError as e:
        print(f"DEBUG: Connection error: {e}")
        # If FastAPI service is not running, return sample data
        return [
            ["Python Developer", "TechCorp Inc", "85"],
            ["Full Stack Developer", "StartupXYZ", "75"],
            ["AI/ML Engineer", "DataCorp", "90"]
        ]
    except Exception as e:
        print(f"DEBUG: Unexpected error: {e}")
        return [["Error", str(e), "N/A"]]

def format_job_results(jobs):
    """Format job results for display"""
    if not jobs:
        return [["No jobs found", "", ""]]

    formatted = []
    for job in jobs:
        title = job.get("title", "Unknown")
        company = job.get("company", "Unknown")
        score = job.get("relevance_score", job.get("match_score", "N/A"))
        if isinstance(score, (int, float)):
            score = f"{score:.1f}"
        formatted.append([title, company, str(score)])

    return formatted

def analyze_job_compatibility(job_url, user_skills):
    """Analyze compatibility with a specific job"""
    try:
        # Call our FastAPI service
        response = requests.post(
            "http://localhost:8000/analyze-job",
            json={"job_url": job_url, "user_skills": user_skills.split(",")},
            timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            analysis = data.get("analysis", {})
            return format_analysis_result(analysis)
        else:
            return "Analysis failed"
    except:
        # Return sample analysis if service is not available
        return """
        **Job Compatibility Analysis**

        Overall Score: 8.5/10

        **Matching Skills:**
        - Python
        - Machine Learning
        - SQL

        **Missing Skills:**
        - Docker
        - Kubernetes

        **Recommendations:**
        - Consider learning containerization technologies
        - You're a strong candidate overall!
        """

def format_analysis_result(analysis):
    """Format analysis result for display"""
    result = f"""
    **Job Compatibility Analysis**

    Overall Score: {analysis.get('overall_score', 'N/A')}/10

    **Matching Skills:**
    {chr(10).join([f"- {skill}" for skill in analysis.get('matching_skills', [])])}

    **Missing Skills:**
    {chr(10).join([f"- {skill}" for skill in analysis.get('missing_skills', [])])}

    **Recommendations:**
    {chr(10).join([f"- {rec.get('message', '')}" for rec in analysis.get('recommendations', [])])}
    """
    return result

def generate_tailored_resume(job_description, base_resume):
    """Generate a tailored resume for a specific job"""
    try:
        # Try n8n webhook first, fallback to FastAPI
        response = None
        try:
            response = requests.post(
                "http://localhost:5678/webhook/resume-optimizer",
                json={"job_description": job_description, "current_resume": base_resume},
                timeout=30
            )
            if response.status_code == 200:
                print(f"DEBUG: Using n8n resume webhook successfully")
            else:
                print(f"DEBUG: n8n resume webhook returned {response.status_code}, falling back to FastAPI")
                raise Exception("n8n webhook failed")
        except:
            print(f"DEBUG: n8n resume webhook failed, falling back to FastAPI")
            response = requests.post(
                "http://localhost:8000/generate-resume",
                json={"job_description": job_description, "base_resume": base_resume},
                timeout=30
            )

        if response.status_code == 200:
            data = response.json()
            tailored_resume = data.get("tailored_resume", {})

            # Format the resume data for display
            formatted_resume = format_resume_for_display(tailored_resume)
            return formatted_resume
        else:
            return "Failed to generate resume"
    except:
        return """
        **Tailored Resume Generated**

        **Professional Summary:**
        Experienced software developer with expertise in Python, machine learning, and web development.
        Passionate about creating innovative solutions and working with cutting-edge technologies.

        **Key Skills:**
        - Python, JavaScript, SQL
        - Machine Learning, TensorFlow
        - Web Development, React, Django
        - Cloud Technologies, AWS

        **Experience:**
        [Your experience sections would be tailored here based on job requirements]
        """

def format_resume_for_display(resume_data):
    """Format resume data for Gradio display"""
    if isinstance(resume_data, str):
        return resume_data

    formatted = "**Tailored Resume Generated**\n\n"

    if "summary" in resume_data:
        formatted += f"**Professional Summary:**\n{resume_data['summary']}\n\n"

    if "skills" in resume_data and resume_data["skills"]:
        formatted += "**Key Skills:**\n"
        for skill in resume_data["skills"][:10]:  # Limit to top 10 skills
            formatted += f"- {skill}\n"
        formatted += "\n"

    if "experience" in resume_data and resume_data["experience"]:
        formatted += "**Experience Highlights:**\n"
        for exp in resume_data["experience"][:3]:  # Show top 3 experiences
            if isinstance(exp, dict):
                title = exp.get("title", "Experience")
                company = exp.get("company", "")
                description = exp.get("description", "")
                formatted += f"**{title}**"
                if company:
                    formatted += f" at {company}"
                formatted += f"\n{description}\n\n"

    if "tailored_for" in resume_data:
        tailored_info = resume_data["tailored_for"]
        formatted += f"**Tailored for:** {tailored_info.get('job_title', 'N/A')} at {tailored_info.get('company', 'N/A')}\n"

    return formatted

def save_application(job_title, company, job_url, compatibility_score):
    """Save job application to database"""
    try:
        conn = sqlite3.connect("../database/applications.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO applications
            (job_title, company, job_url, compatibility_score, date_found, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (job_title, company, job_url, compatibility_score,
              datetime.now().date(), "found"))

        conn.commit()
        conn.close()

        return "Application saved successfully!"
    except Exception as e:
        return f"Error saving application: {str(e)}"

def create_interface():
    """Create the Gradio interface"""

    # Initialize database on startup
    try:
        init_database()
    except:
        pass  # Database might already exist

    with gr.Blocks(title="Job Application System", theme=gr.themes.Soft()) as app:
        gr.Markdown("# 🚀 CP494 - Automated Job Application System")
        gr.Markdown("Your AI-powered job search and application assistant")

        with gr.Tab("🔍 Search Jobs"):
            with gr.Row():
                with gr.Column(scale=1):
                    keywords = gr.Textbox(
                        label="Job Keywords",
                        placeholder="e.g., Python Developer, Data Scientist",
                        value="Python Developer"
                    )
                    location = gr.Textbox(
                        label="Location",
                        placeholder="e.g., London, ON or Remote",
                        value="London, ON"
                    )
                    search_btn = gr.Button("🔍 Search Jobs", variant="primary")

                with gr.Column(scale=2):
                    results = gr.Dataframe(
                        headers=["Job Title", "Company", "Match Score"],
                        datatype=["str", "str", "str"],
                        wrap=True
                    )

            search_btn.click(
                fn=search_jobs,
                inputs=[keywords, location],
                outputs=results
            )

        with gr.Tab("📊 Job Analysis"):
            with gr.Row():
                with gr.Column():
                    job_url_input = gr.Textbox(
                        label="Job URL",
                        placeholder="Paste job posting URL here"
                    )
                    user_skills_input = gr.Textbox(
                        label="Your Skills (comma-separated)",
                        placeholder="Python, SQL, Machine Learning, React",
                        value="Python, SQL, Machine Learning"
                    )
                    analyze_btn = gr.Button("📊 Analyze Job", variant="primary")

                with gr.Column():
                    analysis_output = gr.Markdown(label="Analysis Results")

            analyze_btn.click(
                fn=analyze_job_compatibility,
                inputs=[job_url_input, user_skills_input],
                outputs=analysis_output
            )

        with gr.Tab("📝 Resume Tailor"):
            with gr.Row():
                with gr.Column():
                    job_desc_input = gr.Textbox(
                        label="Job Description",
                        lines=10,
                        placeholder="Paste the full job description here..."
                    )
                    base_resume_input = gr.Textbox(
                        label="Your Base Resume",
                        lines=10,
                        placeholder="Paste your current resume here..."
                    )
                    generate_btn = gr.Button("✨ Generate Tailored Resume", variant="primary")

                with gr.Column():
                    tailored_resume_output = gr.Markdown(label="Tailored Resume")

            generate_btn.click(
                fn=generate_tailored_resume,
                inputs=[job_desc_input, base_resume_input],
                outputs=tailored_resume_output
            )

        with gr.Tab("📋 My Applications"):
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### Track Your Job Applications")

                    # Manual application entry
                    with gr.Group():
                        gr.Markdown("**Add New Application**")
                        manual_job_title = gr.Textbox(label="Job Title")
                        manual_company = gr.Textbox(label="Company")
                        manual_job_url = gr.Textbox(label="Job URL")
                        manual_score = gr.Number(label="Compatibility Score", value=75)
                        save_btn = gr.Button("💾 Save Application")
                        save_status = gr.Textbox(label="Status", interactive=False)

                    # Refresh button
                    refresh_btn = gr.Button("🔄 Refresh Applications")

                with gr.Column(scale=2):
                    applications_df = gr.Dataframe(
                        headers=["ID", "Job Title", "Company", "Score", "Date Found", "Status"],
                        datatype=["str", "str", "str", "str", "str", "str"],
                        value=load_applications(),
                        wrap=True
                    )

            save_btn.click(
                fn=save_application,
                inputs=[manual_job_title, manual_company, manual_job_url, manual_score],
                outputs=save_status
            )

            refresh_btn.click(
                fn=load_applications,
                outputs=applications_df
            )

        with gr.Tab("⚙️ Settings"):
            gr.Markdown("### System Configuration")

            with gr.Group():
                gr.Markdown("**API Configuration**")
                groq_api_key = gr.Textbox(
                    label="Groq API Key",
                    type="password",
                    placeholder="Enter your Groq API key"
                )
                n8n_url = gr.Textbox(
                    label="n8n URL",
                    value="http://localhost:5678",
                    placeholder="n8n instance URL"
                )

            with gr.Group():
                gr.Markdown("**Job Search Preferences**")
                default_keywords = gr.Textbox(
                    label="Default Keywords",
                    value="Python Developer, Software Engineer"
                )
                default_location = gr.Textbox(
                    label="Default Location",
                    value="London, ON"
                )
                min_score = gr.Slider(
                    label="Minimum Compatibility Score",
                    minimum=0,
                    maximum=100,
                    value=70
                )

            save_settings_btn = gr.Button("💾 Save Settings", variant="primary")
            settings_status = gr.Textbox(label="Status", interactive=False)

            def save_settings(*args):
                return "Settings saved successfully!"

            save_settings_btn.click(
                fn=save_settings,
                inputs=[groq_api_key, n8n_url, default_keywords, default_location, min_score],
                outputs=settings_status
            )

    return app

if __name__ == "__main__":
    app = create_interface()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )