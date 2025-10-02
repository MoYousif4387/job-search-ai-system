-- This stores every job you apply to
CREATE TABLE applications (
    id INTEGER PRIMARY KEY,
    job_title TEXT,
    company TEXT,
    job_url TEXT,
    compatibility_score INTEGER,
    date_found DATE,
    date_applied DATE,
    status TEXT  -- 'found', 'applied', 'rejected', 'interview'
);

-- This stores user profile information
CREATE TABLE user_profiles (
    id INTEGER PRIMARY KEY,
    full_name TEXT,
    email TEXT,
    phone TEXT,
    location TEXT,
    linkedin_url TEXT,
    github_url TEXT,
    portfolio_url TEXT,
    skills TEXT, -- JSON array of skills
    experience_years INTEGER,
    education TEXT, -- JSON array of education
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- This stores your different resume versions
CREATE TABLE resumes (
    id INTEGER PRIMARY KEY,
    user_profile_id INTEGER DEFAULT 1,
    job_id INTEGER,
    resume_content TEXT,
    original_filename TEXT,
    file_type TEXT, -- 'pdf', 'docx', 'txt'
    is_base_resume BOOLEAN DEFAULT FALSE,
    cover_letter TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_profile_id) REFERENCES user_profiles (id),
    FOREIGN KEY (job_id) REFERENCES applications (id)
);

-- This stores job search parameters and user preferences
CREATE TABLE user_preferences (
    id INTEGER PRIMARY KEY,
    keywords TEXT,
    location TEXT,
    salary_min INTEGER,
    salary_max INTEGER,
    remote_ok BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- This stores detailed job information
CREATE TABLE job_details (
    id INTEGER PRIMARY KEY,
    application_id INTEGER,
    description TEXT,
    requirements TEXT,
    salary_range TEXT,
    benefits TEXT,
    company_info TEXT,
    job_type TEXT, -- 'full-time', 'part-time', 'contract', 'internship'
    created_at TIMESTAMP,
    FOREIGN KEY (application_id) REFERENCES applications (id)
);

-- This stores analysis results for each job
CREATE TABLE job_analysis (
    id INTEGER PRIMARY KEY,
    application_id INTEGER,
    skill_match_score REAL,
    experience_match_score REAL,
    education_match_score REAL,
    overall_score REAL,
    matching_skills TEXT, -- JSON array of matching skills
    missing_skills TEXT,  -- JSON array of missing skills
    recommendations TEXT, -- JSON array of recommendations
    analysis_date TIMESTAMP,
    FOREIGN KEY (application_id) REFERENCES applications (id)
);