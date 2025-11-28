#!/bin/bash

echo "🔧 Setting up n8n workflows for CP494 Job Application System..."

# Check if n8n is running
if ! curl -s http://localhost:5678 > /dev/null; then
    echo "❌ n8n is not running. Please start it first with: docker compose up -d"
    exit 1
fi

echo "✅ n8n is running"

echo "
📋 Manual Setup Required:

1. Open n8n Dashboard: http://localhost:5678
   Login: admin / password

2. Import Workflows:
   - Click 'New Workflow'
   - Click the three dots menu (⋯)
   - Select 'Import from file'
   - Import these files one by one:
     * n8n-workflows/job-scout.json
     * n8n-workflows/resume-optimizer.json
     * n8n-workflows/main-orchestrator.json

3. Activate Webhooks:
   - For each imported workflow:
     - Click the workflow name
     - Toggle the 'Active' switch (top right)
     - Save the workflow

4. Test the Setup:
   - The job search webhook will be: http://localhost:5678/webhook/search-jobs
   - Test with: curl -X POST http://localhost:5678/webhook/search-jobs -H 'Content-Type: application/json' -d '{\"keywords\":\"python\",\"location\":\"toronto\"}'

🎯 After setup, your system will have:
- ✅ FastAPI service running on port 8000
- ✅ Gradio web interface on port 7860
- ✅ n8n workflows on port 5678
- ✅ Automated job processing pipeline

🚀 Ready to use the complete job application system!
"