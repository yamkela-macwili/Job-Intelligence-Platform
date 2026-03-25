# AI Powered Career and Job Intelligence Platform

## Overview

The AI Powered Career and Job Intelligence Platform is a full stack application that analyzes a user CV against a target job role and generates structured, actionable insights to improve employability.

The system transforms job searching into a data driven process by identifying skill gaps, generating match scores, and producing personalized career recommendations. It combines modern backend engineering with AI and NLP to deliver intelligent decision support.

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

* `React (Vite)` for fast UI development
* `TailwindCSS` for styling
* `Framer Motion` for interactions
* Deployment on `Vercel`

### Backend

* `FastAPI` for high performance APIs
* `Pydantic` for validation and data models

### AI and NLP

* `OpenAI API` for semantic reasoning and generation
* `spaCy` for skill extraction and preprocessing

### File Processing

* `pdfplumber` for extracting text from CV PDFs

### Database

* `PostgreSQL` for relational storage
* `SQLAlchemy` as ORM layer

### Deployment

* Frontend deployed on Vercel
* Backend deployed on Azure App Service
* Database hosted on Azure PostgreSQL

---

## System Architecture

```text
Frontend (React - Vercel)
        ↓
FastAPI Backend (Azure App Service)
        ↓
Service Layer (AI + NLP)
        ↓
PostgreSQL Database (Azure)
```

---

## Project Structure

```text
backend/
│
├── app/
│   ├── main.py
│   │   Entry point of the FastAPI application. Initializes the app and registers routes.
│   │
│   ├── api/
│   │   Contains all API route definitions.
│   │
│   │   ├── routes_cv.py
│   │   │   Handles CV upload and processing endpoints.
│   │   │
│   │   ├── routes_analysis.py
│   │   │   Handles AI analysis requests and responses.
│   │   │
│   │   └── routes_jobs.py
│   │       Handles job input or predefined job roles.
│   │
│   ├── core/
│   │   Core configuration and infrastructure setup.
│   │
│   │   ├── config.py
│   │   │   Manages environment variables and application settings.
│   │   │
│   │   └── database.py
│   │       Initializes database connection and session management.
│   │
│   ├── models/
│   │   Database models using SQLAlchemy.
│   │
│   │   ├── cv.py
│   │   │   Defines the CV table schema.
│   │   │
│   │   ├── analysis.py
│   │   │   Stores analysis results such as match scores and insights.
│   │   │
│   │   └── job.py
│   │       Stores job descriptions or predefined roles.
│   │
│   ├── schemas/
│   │   Pydantic schemas for request and response validation.
│   │
│   │   ├── cv_schema.py
│   │   │   Defines input/output structure for CV operations.
│   │   │
│   │   ├── analysis_schema.py
│   │   │   Defines structure of AI analysis responses.
│   │   │
│   │   └── job_schema.py
│   │       Defines job related request and response formats.
│   │
│   ├── services/
│   │   Core business logic layer.
│   │
│   │   ├── cv_parser.py
│   │   │   Extracts and cleans text from CV PDFs using pdfplumber.
│   │   │
│   │   ├── ai_engine.py
│   │   │   Handles communication with AI models and generates insights.
│   │   │
│   │   ├── job_matcher.py
│   │   │   Computes match scores between CV and job descriptions.
│   │   │
│   │   └── roadmap_generator.py
│   │       Generates career improvement plans based on analysis.
│   │
│   └── utils/
│       └── helpers.py
│           Utility functions used across the application.
│
├── requirements.txt
│   Python dependencies for backend.
│
└── .env
    Environment variables such as database URL and API keys.

frontend/
│
├── src/
│   ├── components/
│   │   Reusable UI components (cards, forms, buttons).
│   │
│   ├── pages/
│   │   Page level components (Landing, Upload, Results).
│   │
│   ├── services/
│   │   Handles API calls to backend.
│   │
│   ├── hooks/
│   │   Custom React hooks for state and logic reuse.
│   │
│   ├── App.jsx
│   │   Root React component.
│   │
│   ├── main.jsx
│   │   Application entry point.
│   │
│   └── index.css
│       Global styles.
│
├── package.json
│   Project dependencies and scripts.
│
└── vite.config.js
    Configuration for Vite build tool.
```

---

## Backend Overview

The backend is built using `FastAPI` and follows a modular architecture.

### Key Responsibilities

* Handle HTTP requests
* Coordinate AI processing
* Manage database interactions
* Return structured responses

The separation of `api`, `services`, and `models` ensures maintainability and scalability.

---

## Database Design

The system uses `PostgreSQL` to persist application data.

### Why a Database Without Authentication

* Avoid repeated AI computations
* Improve response speed through caching
* Enable reuse of previous analyses
* Support future feature expansion

### Core Tables

* `cvs`
  Stores extracted CV content

* `analyses`
  Stores match scores, skill gaps, and recommendations

* `jobs`
  Stores job descriptions

---

## API Endpoints

### POST `/cv/upload`

Uploads and processes a CV file

### POST `/analysis`

Performs AI based analysis

### GET `/analysis`

Retrieves stored analysis results

---

## Setup Instructions

### Prerequisites

* Python 3.10 or higher
* Node.js 18 or higher
* PostgreSQL instance
* OpenAI API key

---

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

Create `.env` file:

```env
DATABASE_URL=your_postgresql_connection_string
OPENAI_API_KEY=your_api_key
```

Run server:

```bash
uvicorn app.main:app --reload
```

---

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

---

## Deployment

### Frontend

Deployed on Vercel for fast global delivery

### Backend

Deployed on Azure App Service

### Database

Hosted on Azure Database for PostgreSQL

---

## Performance Strategy

The system minimizes redundant AI calls by caching analysis results in the database. When similar inputs are detected, stored results are returned instead of recomputing them.

---

## License

This project is licensed under the MIT License.

This means the software can be used, modified, and distributed freely, provided that the original license and copyright notice are included.

---

## Future Improvements

* User authentication and dashboards
* Analysis history and comparison
* AI career assistant
* Integration with job platforms
* Advanced analytics

---

## Contribution

Contributions are welcome. Fork the repository, create a feature branch, and submit a pull request with clear descriptions of changes.
