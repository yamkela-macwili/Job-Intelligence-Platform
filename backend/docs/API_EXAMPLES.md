# API Usage Examples

Complete examples for using the Job Intelligence Platform API.

---

## Base URL

```
http://localhost:8000/api/v1
https://yourdomain.com/api/v1  (production)
```

---

## Authentication

Currently, the API uses no authentication (design choice for this phase).
For production, add JWT authentication:

```python
# Add to main.py
from fastapi.security import HTTPBearer, HTTPAuthCredential
security = HTTPBearer()
```

---

## Health Endpoints

### 1. Health Check
```bash
curl -X GET http://localhost:8000/health

# Response (200 OK)
{
  "status": "OK",
  "service": "Job Intelligence Platform API",
  "version": "1.0.0"
}
```

### 2. Readiness Check
```bash
curl -X GET http://localhost:8000/ready

# Response (200 OK)
{
  "ready": true,
  "service": "Job Intelligence Platform API"
}
```

### 3. API Information
```bash
curl -X GET http://localhost:8000/

# Response (200 OK)
{
  "message": "Welcome to Job Intelligence Platform API",
  "version": "1.0.0",
  "documentation": "/docs",
  "endpoints": {
    "health": "/health",
    "cv": "/api/v1/cv",
    "jobs": "/api/v1/jobs",
    "analysis": "/api/v1/analysis"
  }
}
```

---

## CV Operations

### 1. Upload CV (PDF)

**Endpoint**: `POST /cv/upload`

**Request**:
```bash
curl -X POST "http://localhost:8000/api/v1/cv/upload" \
  -F "file=@resume.pdf"
```

**Response (201 Created)**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "resume.pdf",
  "message": "CV uploaded and processed successfully",
  "created_at": "2024-03-25T10:30:00"
}
```

**Error Responses**:
```bash
# Invalid file type (400)
{
  "detail": "Only PDF files are accepted"
}

# File too large (413)
{
  "detail": "File size exceeds maximum allowed size of 52428800 bytes"
}

# Processing error (500)
{
  "detail": "Error processing CV file"
}
```

---

### 2. List CVs with Pagination

**Endpoint**: `GET /cv`

**Request**:
```bash
curl -X GET "http://localhost:8000/api/v1/cv?skip=0&limit=10"
```

**Query Parameters**:
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum records to return (default: 10, max: 100)

**Response (200 OK)**:
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "filename": "resume.pdf",
    "raw_text": "John Doe\n...",
    "processed_text": "John Doe...",
    "skills_extracted": ["Python", "FastAPI", "PostgreSQL"],
    "created_at": "2024-03-25T10:30:00"
  },
  {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "filename": "resume_v2.pdf",
    "raw_text": "Jane Smith\n...",
    "processed_text": "Jane Smith...",
    "skills_extracted": ["Java", "Spring", "Docker"],
    "created_at": "2024-03-25T11:00:00"
  }
]
```

---

### 3. Get Specific CV

**Endpoint**: `GET /cv/{id}`

**Request**:
```bash
curl -X GET "http://localhost:8000/api/v1/cv/550e8400-e29b-41d4-a716-446655440000"
```

**Response (200 OK)**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "resume.pdf",
  "raw_text": "John Doe\nSoftware Engineer...",
  "processed_text": "John Doe Software Engineer...",
  "skills_extracted": ["Python", "FastAPI", "PostgreSQL"],
  "created_at": "2024-03-25T10:30:00"
}
```

**Error Response (404 Not Found)**:
```json
{
  "detail": "CV not found"
}
```

---

### 4. Delete CV

**Endpoint**: `DELETE /cv/{id}`

**Request**:
```bash
curl -X DELETE "http://localhost:8000/api/v1/cv/550e8400-e29b-41d4-a716-446655440000"
```

**Response (204 No Content)**: Empty response

---

## Job Operations

### 1. Create Job

**Endpoint**: `POST /jobs`

**Request**:
```bash
curl -X POST "http://localhost:8000/api/v1/jobs" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Senior Python Developer",
    "description": "We are looking for a senior Python developer with 5+ years of experience in building scalable web applications. Required skills: Python, FastAPI, PostgreSQL, Docker, AWS. Nice to have: Kubernetes, Redis."
  }'
```

**Response (201 Created)**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "title": "Senior Python Developer",
  "message": "Job created successfully",
  "created_at": "2024-03-25T10:35:00"
}
```

**Error Response (500)**:
```json
{
  "detail": "Error creating job entry"
}
```

---

### 2. List Jobs

**Endpoint**: `GET /jobs`

**Request**:
```bash
curl -X GET "http://localhost:8000/api/v1/jobs?skip=0&limit=5"
```

**Response (200 OK)**:
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "title": "Senior Python Developer",
    "description": "We are looking for...",
    "skills_required": ["Python", "FastAPI", "PostgreSQL", "Docker", "AWS"],
    "created_at": "2024-03-25T10:35:00"
  }
]
```

---

### 3. Get Specific Job

**Endpoint**: `GET /jobs/{id}`

**Request**:
```bash
curl -X GET "http://localhost:8000/api/v1/jobs/550e8400-e29b-41d4-a716-446655440001"
```

**Response (200 OK)**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "title": "Senior Python Developer",
  "description": "We are looking for...",
  "skills_required": ["Python", "FastAPI", "PostgreSQL", "Docker", "AWS"],
  "created_at": "2024-03-25T10:35:00"
}
```

---

### 4. Update Job

**Endpoint**: `PUT /jobs/{id}`

**Request**:
```bash
curl -X PUT "http://localhost:8000/api/v1/jobs/550e8400-e29b-41d4-a716-446655440001" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Senior Python Developer (Updated)",
    "description": "Updated description..."
  }'
```

**Response (200 OK)**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "title": "Senior Python Developer (Updated)",
  "description": "Updated description...",
  "skills_required": ["Python", "FastAPI", "PostgreSQL"],
  "created_at": "2024-03-25T10:35:00"
}
```

---

### 5. Delete Job

**Endpoint**: `DELETE /jobs/{id}`

**Request**:
```bash
curl -X DELETE "http://localhost:8000/api/v1/jobs/550e8400-e29b-41d4-a716-446655440001"
```

**Response (204 No Content)**: Empty response

---

## Analysis Operations

### 1. Create Analysis (CV vs Job)

**Endpoint**: `POST /analysis`

**Request Option 1 - With Job ID**:
```bash
curl -X POST "http://localhost:8000/api/v1/analysis" \
  -H "Content-Type: application/json" \
  -d '{
    "cv_id": "550e8400-e29b-41d4-a716-446655440000",
    "job_id": "550e8400-e29b-41d4-a716-446655440001"
  }'
```

**Request Option 2 - With Job Description**:
```bash
curl -X POST "http://localhost:8000/api/v1/analysis" \
  -H "Content-Type: application/json" \
  -d '{
    "cv_id": "550e8400-e29b-41d4-a716-446655440000",
    "job_description": "Looking for Python developer with 3+ years experience..."
  }'
```

**Response (201 Created)**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440002",
  "cv_id": "550e8400-e29b-41d4-a716-446655440000",
  "job_id": "550e8400-e29b-41d4-a716-446655440001",
  "match_score": 78,
  "missing_skills": [
    {
      "skill": "Kubernetes",
      "importance": "high"
    },
    {
      "skill": "Docker",
      "importance": "high"
    },
    {
      "skill": "Redis",
      "importance": "medium"
    }
  ],
  "strengths": [
    {
      "skill": "Python",
      "proficiency": "expert"
    },
    {
      "skill": "FastAPI",
      "proficiency": "advanced"
    },
    {
      "skill": "PostgreSQL",
      "proficiency": "advanced"
    }
  ],
  "recommendations": "Focus on containerization technologies like Docker and Kubernetes. These are crucial for the Senior Python Developer role. Consider taking a course on Docker fundamentals and Kubernetes orchestration. Additionally, gaining experience with Redis for caching will significantly improve your candidacy.",
  "roadmap": "## Career Development Roadmap\n\n### Phase 1: Foundation (Months 1-4)\nFocus: Building foundational knowledge\n\nKey Skills to Learn:\n1. Docker (High Priority)\n2. Kubernetes (High Priority)\n3. Redis (Medium Priority)...",
  "created_at": "2024-03-25T10:40:00"
}
```

**Error Responses**:
```bash
# CV not found (404)
{
  "detail": "CV not found"
}

# Job not found (404)
{
  "detail": "Job not found"
}

# Missing both job_id and job_description (400)
{
  "detail": "Either job_id or job_description must be provided"
}

# Analysis error (500)
{
  "detail": "Error performing analysis"
}
```

---

### 2. List Analyses

**Endpoint**: `GET /analysis`

**Request**:
```bash
curl -X GET "http://localhost:8000/api/v1/analysis?skip=0&limit=10"
```

**Query Parameters**:
- `skip` (optional): Number of records to skip
- `limit` (optional): Maximum records to return
- `cv_id` (optional): Filter by CV ID
- `job_id` (optional): Filter by Job ID

**Examples**:
```bash
# All analyses
curl "http://localhost:8000/api/v1/analysis"

# Analyses for specific CV
curl "http://localhost:8000/api/v1/analysis?cv_id=550e8400-e29b-41d4-a716-446655440000"

# Analyses for specific Job
curl "http://localhost:8000/api/v1/analysis?job_id=550e8400-e29b-41d4-a716-446655440001"

# With pagination
curl "http://localhost:8000/api/v1/analysis?skip=10&limit=20"
```

**Response (200 OK)**:
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440002",
    "cv_id": "550e8400-e29b-41d4-a716-446655440000",
    "job_id": "550e8400-e29b-41d4-a716-446655440001",
    "match_score": 78,
    "missing_skills": [...],
    "strengths": [...],
    "recommendations": "...",
    "roadmap": "...",
    "created_at": "2024-03-25T10:40:00"
  }
]
```

---

### 3. Get Specific Analysis

**Endpoint**: `GET /analysis/{id}`

**Request**:
```bash
curl -X GET "http://localhost:8000/api/v1/analysis/550e8400-e29b-41d4-a716-446655440002"
```

**Response (200 OK)**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440002",
  "cv_id": "550e8400-e29b-41d4-a716-446655440000",
  "job_id": "550e8400-e29b-41d4-a716-446655440001",
  "match_score": 78,
  "missing_skills": [
    {"skill": "Kubernetes", "importance": "high"}
  ],
  "strengths": [
    {"skill": "Python", "proficiency": "expert"}
  ],
  "recommendations": "...",
  "roadmap": "...",
  "created_at": "2024-03-25T10:40:00"
}
```

---

### 4. Delete Analysis

**Endpoint**: `DELETE /analysis/{id}`

**Request**:
```bash
curl -X DELETE "http://localhost:8000/api/v1/analysis/550e8400-e29b-41d4-a716-446655440002"
```

**Response (204 No Content)**: Empty response

---

## Complete Workflow Example

```bash
#!/bin/bash

BASE_URL="http://localhost:8000/api/v1"

# Step 1: Upload CV
echo "1. Uploading CV..."
CV_RESPONSE=$(curl -s -X POST "$BASE_URL/cv/upload" \
  -F "file=@resume.pdf")
CV_ID=$(echo $CV_RESPONSE | jq -r '.id')
echo "CV ID: $CV_ID"

# Step 2: Create Job
echo -e "\n2. Creating Job..."
JOB_RESPONSE=$(curl -s -X POST "$BASE_URL/jobs" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Senior Python Developer",
    "description": "5+ years Python experience required..."
  }')
JOB_ID=$(echo $JOB_RESPONSE | jq -r '.id')
echo "Job ID: $JOB_ID"

# Step 3: Run Analysis
echo -e "\n3. Running Analysis..."
ANALYSIS_RESPONSE=$(curl -s -X POST "$BASE_URL/analysis" \
  -H "Content-Type: application/json" \
  -d "{
    \"cv_id\": \"$CV_ID\",
    \"job_id\": \"$JOB_ID\"
  }")
ANALYSIS_ID=$(echo $ANALYSIS_RESPONSE | jq -r '.id')
MATCH_SCORE=$(echo $ANALYSIS_RESPONSE | jq -r '.match_score')
echo "Analysis ID: $ANALYSIS_ID"
echo "Match Score: $MATCH_SCORE"

# Step 4: Get Analysis Details
echo -e "\n4. Getting Analysis Details..."
curl -s -X GET "$BASE_URL/analysis/$ANALYSIS_ID" | jq .

echo -e "\nWorkflow completed!"
```

---

## Rate Limiting (When Implemented)

Expected rate limits:
- 100 requests per minute per IP
- 10,000 requests per day per IP
- 5 MB file upload limit

Response headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1711353600
```

---

## Response Time Expectations

- CV Upload: 3-8 seconds (depends on PDF size)
- Job Creation: 1-3 seconds (AI processing)
- Analysis: 5-15 seconds (AI analysis + matching)
- Cached Analysis: <500ms (if exists)
- List Operations: <1 second

---

## Pagination Best Practices

```bash
# Get first page
curl "http://localhost:8000/api/v1/cv?skip=0&limit=20"

# Get next page
curl "http://localhost:8000/api/v1/cv?skip=20&limit=20"

# Get with different limit
curl "http://localhost:8000/api/v1/cv?skip=0&limit=50"
```

---

## Error Handling

All errors follow this format:
```json
{
  "detail": "Error message describing the issue"
}
```

Common HTTP Status Codes:
- 200: Success
- 201: Created
- 204: No Content
- 400: Bad Request (validation error)
- 404: Not Found
- 413: Payload Too Large
- 500: Internal Server Error

---

## Python Client Example

```python
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

class JobIntelligenceClient:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
    
    def upload_cv(self, file_path):
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{self.base_url}/cv/upload", files=files)
        return response.json()
    
    def create_job(self, title, description):
        data = {
            "title": title,
            "description": description
        }
        response = requests.post(f"{self.base_url}/jobs", json=data)
        return response.json()
    
    def analyze(self, cv_id, job_id=None, job_description=None):
        data = {
            "cv_id": cv_id,
            "job_id": job_id,
            "job_description": job_description
        }
        response = requests.post(f"{self.base_url}/analysis", json=data)
        return response.json()
    
    def get_analysis(self, analysis_id):
        response = requests.get(f"{self.base_url}/analysis/{analysis_id}")
        return response.json()

# Usage
client = JobIntelligenceClient()

# Upload CV
cv_result = client.upload_cv("resume.pdf")
cv_id = cv_result['id']

# Create job
job_result = client.create_job(
    "Senior Developer",
    "Looking for 5+ years experience..."
)
job_id = job_result['id']

# Run analysis
analysis = client.analyze(cv_id, job_id)
print(f"Match Score: {analysis['match_score']}")
```

---

Last Updated: March 25, 2024
