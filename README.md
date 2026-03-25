# AI Powered Career and Job Intelligence Platform

## Overview

The AI Powered Career and Job Intelligence Platform is a full stack application that analyzes a user CV against a target job role and generates structured, actionable insights to improve employability.

The system transforms job searching into a data driven process by identifying skill gaps, generating match scores, and producing personalized career recommendations. It combines backend engineering, AI, and NLP into a scalable architecture.

This version introduces containerization using Docker for the backend to ensure consistency, portability, and simplified deployment.

---

## Core Features

* CV upload and parsing from PDF files
* Job role selection or custom job description input
* AI powered job match scoring
* Skill gap identification
* Career roadmap generation
* CV improvement suggestions
* Persistent storage of CV data and analysis results
* Optimized performance through caching of AI outputs

---

## Tech Stack

### Frontend

* `React (Vite)`
* `TailwindCSS`
* `Framer Motion`
* Deployment on `Vercel`

### Backend

* `FastAPI`
* `Pydantic`
* Containerized with `Docker`

### AI and NLP

* `OpenAI API`
* `spaCy`

### File Processing

* `pdfplumber`

### Database

* `PostgreSQL`
* `SQLAlchemy`

### Deployment

* Frontend deployed on Vercel
* Backend container deployed on Azure
* Database hosted on Azure PostgreSQL

---

## System Architecture

```text id="t1r92q"
Frontend (React - Vercel)
        ↓
Dockerized FastAPI Backend (Azure)
        ↓
Service Layer (AI + NLP)
        ↓
PostgreSQL Database (Azure)
```

---

## Project Structure

```text id="7rd4qp"
backend/
│
├── app/
│   ├── main.py
│   │   Entry point of the FastAPI application. Initializes app and routes.
│   │
│   ├── api/
│   │   ├── routes_cv.py
│   │   │   Handles CV upload endpoints.
│   │   │
│   │   ├── routes_analysis.py
│   │   │   Handles AI analysis requests.
│   │   │
│   │   └── routes_jobs.py
│   │       Handles job related inputs.
│   │
│   ├── core/
│   │   ├── config.py
│   │   │   Environment configuration.
│   │   │
│   │   └── database.py
│   │       Database connection setup.
│   │
│   ├── models/
│   │   ├── cv.py
│   │   │   CV table definition.
│   │   │
│   │   ├── analysis.py
│   │   │   Analysis results schema.
│   │   │
│   │   └── job.py
│   │       Job descriptions schema.
│   │
│   ├── schemas/
│   │   ├── cv_schema.py
│   │   ├── analysis_schema.py
│   │   └── job_schema.py
│   │
│   ├── services/
│   │   ├── cv_parser.py
│   │   │   Extracts CV text using pdfplumber.
│   │   │
│   │   ├── ai_engine.py
│   │   │   Handles AI interactions.
│   │   │
│   │   ├── job_matcher.py
│   │   │   Computes match scores.
│   │   │
│   │   └── roadmap_generator.py
│   │       Generates improvement plans.
│   │
│   └── utils/
│       └── helpers.py
│
├── Dockerfile
│   Defines backend container image.
│
├── .dockerignore
│   Excludes unnecessary files from image.
│
├── requirements.txt
│   Backend dependencies.
│
└── .env
    Environment variables.

frontend/
│
├── src/
│   ├── components/
│   ├── pages/
│   ├── services/
│   ├── hooks/
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
│
├── package.json
└── vite.config.js
```

---

## Backend Containerization

### Dockerfile

```dockerfile id="p7d1hf"
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

### .dockerignore

```text id="2n2n4m"
__pycache__/
*.pyc
*.pyo
*.pyd
.env
venv/
```

---

## Running Backend with Docker

### Build Image

```bash id="3h4c6q"
docker build -t career-ai-backend .
```

### Run Container

```bash id="9tq1xl"
docker run -d -p 8000:8000 --env-file .env career-ai-backend
```

---

## Backend Overview

The backend uses FastAPI and follows a modular service oriented architecture.

Responsibilities include:

* API routing
* AI orchestration
* Data persistence
* CV processing

Docker ensures:

* Environment consistency
* Easy deployment
* Isolation of dependencies

---

## Database Design

The system uses PostgreSQL for persistent storage.

### Purpose

* Cache AI results
* Store CV content
* Improve performance
* Enable future features

### Core Tables

* `cvs`
* `analyses`
* `jobs`

---

## API Endpoints

### POST `/cv/upload`

Uploads and processes CV

### POST `/analysis`

Performs AI analysis

### GET `/analysis`

Fetches stored results

---

## Setup Instructions

### Prerequisites

* Docker
* Node.js
* PostgreSQL
* OpenAI API key

---

### Backend Setup with Docker

```bash id="h7t9yk"
cd backend
docker build -t career-ai-backend .
docker run -p 8000:8000 --env-file .env career-ai-backend
```

---

### Frontend Setup

```bash id="w8k2mf"
cd frontend
npm install
npm run dev
```

---

## Deployment

### Frontend

Deploy on Vercel

### Backend

Deploy Docker container to Azure App Service or Azure Container Apps

### Database

Azure Database for PostgreSQL

---

## Performance Strategy

* Cache AI outputs in PostgreSQL
* Avoid redundant API calls
* Preprocess CV text before AI usage

---

## License

This project is licensed under the MIT License.

---

## Future Improvements

* Authentication system
* Analysis history
* AI assistant
* Job recommendation engine
* Advanced analytics

---

## Contribution

Fork the repository and submit pull requests with clear documentation.
