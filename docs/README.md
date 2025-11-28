# 🚀 CP494 - Automated Job Application System

## 📋 Project Overview

This is a comprehensive AI-powered job application automation system that:
- **Automatically searches** for relevant job opportunities
- **Analyzes job compatibility** using AI agents
- **Tailors resumes** for specific job requirements
- **Tracks applications** in a centralized database
- **Provides insights** through an intuitive web interface

## 🏗️ Architecture

```
CP494-project/
├── docker-compose.yml          # n8n orchestration
├── .env                        # Environment variables
├── n8n-workflows/              # Automation workflows
├── crews/                      # AI agents (CrewAI)
├── database/                   # SQLite database
├── ui/                        # Gradio web interface
└── docs/                      # Documentation
```

## 🔧 Technology Stack

- **Orchestration**: n8n (workflow automation)
- **AI Agents**: CrewAI + Groq (free LLM access)
- **Database**: SQLite
- **Frontend**: Gradio
- **Containerization**: Docker

## 🚀 Quick Start

### 1. Start n8n Service
```bash
cd CP494-project
docker-compose up -d
```

### 2. Access n8n Dashboard
- Open: http://localhost:5678
- Login: admin / password

### 3. Install Python Dependencies
```bash
pip install crewai langchain-groq gradio requests sqlite3
```

### 4. Start the UI
```bash
cd ui
python app.py
```

### 5. Access the Interface
- Open: http://localhost:7860

## 📊 Features

### 🔍 Job Search
- Automated job discovery from multiple sources
- Keyword and location-based filtering
- Real-time compatibility scoring

### 📊 Smart Analysis
- AI-powered job requirement extraction
- Skill gap analysis
- Personalized recommendations

### 📝 Resume Optimization
- Automatic resume tailoring
- Keyword optimization
- Cover letter generation

### 📋 Application Tracking
- Centralized application database
- Status tracking (found → applied → interview → hired)
- Analytics and insights

## 🔧 Configuration

### Environment Variables (.env)
```bash
# Your Groq API key (FREE)
GROQ_API_KEY=your_groq_api_key_here

# n8n settings
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=password
N8N_PORT=5678
```

### User Profile Setup
1. Add your skills in the UI settings
2. Upload your base resume
3. Set job search preferences
4. Configure notification preferences

## 🤖 AI Agents

### Job Scout Agent
- **Role**: Finds relevant job opportunities
- **Skills**: Web scraping, keyword matching, relevance scoring
- **Output**: Filtered job listings with compatibility scores

### Analyzer Agent
- **Role**: Analyzes job-candidate compatibility
- **Skills**: NLP, requirement extraction, gap analysis
- **Output**: Detailed compatibility reports with recommendations

### Resume Writer Agent
- **Role**: Creates tailored resumes and cover letters
- **Skills**: Content optimization, keyword integration, formatting
- **Output**: Customized application materials

## 📈 Workflows

### Main Orchestrator
1. **Trigger**: Runs every 6 hours
2. **Job Discovery**: Calls job scout agent
3. **Analysis**: Evaluates each job opportunity
4. **Filtering**: Scores above 70% trigger resume generation
5. **Storage**: Saves all data to database

### Resume Generation
1. **Input**: Job description + base resume
2. **Analysis**: Extract job requirements
3. **Optimization**: Tailor content and keywords
4. **Output**: Customized resume + cover letter

## 🗄️ Database Schema

### Applications Table
- Job details and compatibility scores
- Application status tracking
- Date tracking

### Resumes Table
- Version control for tailored resumes
- Job-specific customizations

### Analysis Table
- AI analysis results
- Skill gap assessments
- Recommendations

## 🎯 Usage Examples

### Search for Jobs
```python
# Via UI: Enter keywords like "Python Developer"
# Via API: POST to n8n webhook with search criteria
```

### Analyze Compatibility
```python
# Upload job description
# System returns compatibility score and recommendations
```

### Generate Tailored Resume
```python
# Input: Base resume + job description
# Output: Optimized resume highlighting relevant skills
```

## 🔍 Troubleshooting

### n8n Won't Start
- Check Docker is running
- Verify port 5678 is available
- Check docker-compose.yml configuration

### UI Connection Issues
- Ensure Gradio app is running on port 7860
- Check firewall settings
- Verify Python dependencies

### AI Agents Not Working
- Confirm Groq API key is valid
- Check internet connection
- Verify CrewAI installation

## 📚 Learning Objectives (CP494)

This project demonstrates:
- **Workflow Automation**: Using n8n for complex business processes
- **AI Integration**: Leveraging LLMs for intelligent decision making
- **Data Management**: Structured storage and retrieval
- **User Experience**: Building intuitive interfaces
- **System Architecture**: Designing scalable, maintainable systems

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is for educational purposes as part of CP494 coursework.

## 🆘 Support

- **Issues**: Check troubleshooting section
- **Documentation**: See `/docs` folder
- **Course Help**: Contact instructor or TAs

---

**Built with ❤️ for CP494 - Advanced Software Engineering**