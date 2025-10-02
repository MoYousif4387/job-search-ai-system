# 🎯 CP494 Demo Guide

**For Professor Meeting - Quick Access Instructions**

---

## 🚀 Quick Demo Startup

### **Option 1: Automated Demo Script**
```bash
cd /Users/mahmoud/job-search-ai/CP494-project-demo
./start_demo.sh
```

### **Option 2: Manual Startup**
```bash
# Terminal 1 - Start API Service
cd /Users/mahmoud/job-search-ai/CP494-project-demo
python3 simple_api_service.py

# Terminal 2 - Start Web Interface
cd /Users/mahmoud/job-search-ai/CP494-project-demo/ui
python3 app.py
```

---

## 📱 Access Points

| Service | URL | Purpose |
|---------|-----|---------|
| **Main Demo** | http://localhost:7861 | Primary web interface |
| **API Docs** | http://localhost:8001/docs | Backend API documentation |
| **Health Check** | http://localhost:8001/health | System status verification |

---

## 🎭 Demo Features to Showcase

### **1. Job Search Engine**
- **Location:** "Search Jobs" tab
- **Test Query:** "software intern" in "Toronto"
- **Expected Results:** 6+ internship/new grad positions
- **Sources:** Indeed, LinkedIn, Government, Universities

### **2. Job Analysis**
- **Location:** "Job Analysis" tab
- **Test URL:** Any job posting URL
- **Test Skills:** "Python, SQL, Machine Learning"
- **Expected:** Compatibility score and recommendations

### **3. Resume Tailoring**
- **Location:** "Resume Tailor" tab
- **Test:** Paste job description and sample resume
- **Expected:** Customized resume and cover letter

### **4. Application Tracking**
- **Location:** "My Applications" tab
- **Feature:** Add/view saved applications
- **Expected:** Database-backed application management

---

## 🔧 Demo System Status

**✅ Working Features:**
- Multi-source job search with real results
- Job compatibility analysis
- AI-powered resume tailoring
- Application tracking system
- Professional web interface

**🚧 In Development:**
- Resume file upload (PDF/DOCX parsing)
- Real job URL content analysis
- n8n workflow automation
- PDF export functionality

---

## 📊 Sample Demo Data

### **Job Search Results**
- **Shopify:** Software Engineering Intern - Summer 2025
- **RBC:** Data Science Intern
- **Vector Institute:** ML Research Intern
- **Government of Canada:** IT Student Co-op
- **AWS:** Cloud Infrastructure Intern

### **Skills Analysis**
- **Matching Skills:** Python, JavaScript, SQL
- **Missing Skills:** Docker, Kubernetes, AWS
- **Compatibility Score:** 75-95% range

---

## 🎯 Key Points for Professor

### **Current Capabilities**
1. **Real Job Integration:** Live data from multiple job boards
2. **AI Analysis:** Groq API integration for intelligent matching
3. **Professional Interface:** Clean, intuitive web design
4. **Database Management:** Persistent application tracking

### **Technical Architecture**
- **Frontend:** Gradio-based web interface
- **Backend:** FastAPI RESTful services
- **AI Integration:** Groq LLM for analysis
- **Data Storage:** SQLite database
- **Automation:** n8n workflow engine (ready for activation)

### **Research Innovation**
- **Multi-source Aggregation:** Unified job search across platforms
- **AI-Powered Matching:** Intelligent compatibility analysis
- **Automated Workflows:** End-to-end application automation
- **Real-time Processing:** Fast, responsive job discovery

---

## 🔍 Demo Troubleshooting

### **If Demo Doesn't Start:**
```bash
# Check if ports are in use
lsof -ti:7861 -ti:8001 | xargs kill -9 2>/dev/null

# Restart demo
cd /Users/mahmoud/job-search-ai/CP494-project-demo
./start_demo.sh
```

### **If No Job Results:**
- FastAPI service should show "Found X real jobs" in console
- Check API status at http://localhost:8001/health
- Gradio should show real job listings, not "No jobs found"

### **Expected Console Output:**
```
✅ Demo system is now running!
📱 Gradio Interface: http://localhost:7861
📊 FastAPI Docs: http://localhost:8001/docs
```

---

## 📈 Development Roadmap

### **Phase 1: Enhanced Resume Management**
- File upload system (PDF, DOCX, TXT)
- AI skill extraction from resumes
- Real user profile management

### **Phase 2: Advanced Job Analysis**
- Web scraping for job URL content
- AI-powered job description parsing
- Improved compatibility algorithms

### **Phase 3: Workflow Automation**
- n8n workflow activation
- Automated job discovery
- End-to-end application processing

### **Phase 4: Export & Analytics**
- PDF resume/cover letter generation
- Application success analytics
- Interview preparation tools

---

## 📞 Support During Demo

**If Issues Arise:**
1. **Check Console Logs:** Both FastAPI and Gradio terminals
2. **Verify Services:** Ensure both services are running
3. **Restart if Needed:** Use kill commands above and restart
4. **Fallback:** Show API documentation at `/docs` endpoint

**Demo Duration:** ~10-15 minutes for full feature showcase

---

*Demo Version Preserved: January 2025*
*Main Development: https://github.com/MoYousif4387/CP494-job-application-system*