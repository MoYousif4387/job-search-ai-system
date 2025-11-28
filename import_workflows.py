#!/usr/bin/env python3
"""
Import n8n workflows via API
"""

import requests
import json
import os

# n8n API configuration
N8N_URL = "http://localhost:5678"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI5YzU0MDlhYy0yOWYwLTRiOTEtODU1Zi1lOGRlNDU2Njg0YTkiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzU5MzYyNzg2fQ.ouDq7MCwEh81dsJtgq3xS-7nQYnDh79ITWIVwuXGr4Y"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def import_workflow(workflow_file):
    """Import a single workflow file"""
    try:
        print(f"📁 Reading {workflow_file}...")
        with open(workflow_file, 'r') as f:
            workflow_data = json.load(f)

        print(f"🚀 Importing workflow: {workflow_data.get('name', 'Unknown')}")

        response = requests.post(
            f"{N8N_URL}/api/workflows",
            headers=headers,
            json=workflow_data
        )

        if response.status_code == 201:
            result = response.json()
            print(f"✅ Successfully imported: {workflow_data['name']} (ID: {result.get('id')})")
            return True
        else:
            print(f"❌ Failed to import {workflow_data['name']}: {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Error importing {workflow_file}: {str(e)}")
        return False

def main():
    print("🔧 n8n Workflow Importer")
    print("=" * 40)

    # Check if n8n is accessible
    try:
        response = requests.get(f"{N8N_URL}/api/workflows", headers=headers)
        if response.status_code != 200:
            print(f"❌ Cannot access n8n API. Status: {response.status_code}")
            print("Make sure n8n is running and the API key is correct.")
            return
    except Exception as e:
        print(f"❌ Cannot connect to n8n: {str(e)}")
        return

    print("✅ Connected to n8n API")

    # Import workflows
    workflow_files = [
        "n8n-workflows/job-scout.json",
        "n8n-workflows/resume-optimizer.json",
        "n8n-workflows/main-orchestrator.json"
    ]

    successful_imports = 0
    for workflow_file in workflow_files:
        if os.path.exists(workflow_file):
            if import_workflow(workflow_file):
                successful_imports += 1
        else:
            print(f"❌ File not found: {workflow_file}")

    print("=" * 40)
    print(f"✅ Import complete: {successful_imports}/{len(workflow_files)} workflows imported")

    if successful_imports > 0:
        print("\n🎯 Next steps:")
        print("1. Open n8n at http://localhost:5678")
        print("2. Go to your workflows list")
        print("3. Activate the imported workflows")
        print("4. Test the webhook endpoints")

if __name__ == "__main__":
    main()