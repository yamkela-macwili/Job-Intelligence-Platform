# Job Intelligence Platform - Backend Implementation

Production-ready backend for AI-powered career and job intelligence platform using FastAPI, PostgreSQL, SQLAlchemy, and Docker.

## Architecture Overview

### Layered Architecture
```
API Layer (FastAPI Routes)
    ↓
Service Layer (Business Logic)
    ↓
Data Layer (SQLAlchemy Models)
    ↓
Database Layer (PostgreSQL)
```

### Project Structure
```
backend/
├── app/
│   ├── api/
│   │   ├── routes_cv.py          # CV upload and retrieval
│   │   ├── routes_jobs.py        # Job management
│   │   └── routes_analysis.py    # AI analysis endpoints
│   └── main.py                   # FastAPI application entry point
├── core/
│   ├── config.py                 # Configuration management
│   └── database.py               # Database connection and session
├── models/
│   ├── cv.py                     # CV SQLAlchemy model
│   ├── job.py                    # Job SQLAlchemy model
│   └── analysis.py               # Analysis SQLAlchemy model
├── schemas/
│   ├── cv_schema.py              # CV Pydantic schemas
│   ├── job_schema.py             # Job Pydantic schemas
│   └── analysis_schema.py        # Analysis Pydantic schemas
├── services/
│   ├── cv_parser.py              # CV PDF extraction and parsing
│   ├── ai_engine.py              # OpenAI integration
│   ├── job_matcher.py            # Job-CV compatibility scoring
│   └── roadmap_generator.py      # Career roadmap generation
├── utils/
│   └── helpers.py                # Utility functions
├── Dockerfile                    # Container configuration
├── requirements.txt              # Python dependencies
└── .env                          # Environment variables
```

## Core Features

### 1. CV Upload & Processing
- **Endpoint**: `POST /api/v1/cv/upload`
- Extract text from PDF using pdfplumber
- Clean and normalize text
- Extract skills using spaCy NLP
- Extract contact information
- Store in PostgreSQL

### 2. Job Management
- **Endpoints**: 
  - `POST /api/v1/jobs` - Create job
  - `GET /api/v1/jobs` - List jobs
  - `GET /api/v1/jobs/{id}` - Get job details
  - `PUT /api/v1/jobs/{id}` - Update job
  - `DELETE /api/v1/jobs/{id}` - Delete job
- Accept job title and description
- Extract required skills using AI
- Store in database

### 3. AI-Powered Analysis
- **Endpoint**: `POST /api/v1/analysis`
- Match CV against job requirements
- Calculate compatibility score (0-100)
- Identify missing skills with importance levels
- Identify CV strengths
- Generate personalized recommendations
- Create career development roadmap

### 4. Caching Strategy
- Check for similar analyses before AI calls
- Cache results for 24 hours (configurable)
- Reduce API costs and latency
- TTL-based cache invalidation

## API Endpoints

### Health & Status
```
GET /health                          # Health check
GET /ready                           # Readiness probe
GET /                                # API information
```

### CV Operations
```
POST   /api/v1/cv/upload            # Upload CV PDF
GET    /api/v1/cv                   # List all CVs
GET    /api/v1/cv/{id}              # Get CV details
DELETE /api/v1/cv/{id}              # Delete CV
```

### Job Operations
```
POST   /api/v1/jobs                 # Create job
GET    /api/v1/jobs                 # List jobs
GET    /api/v1/jobs/{id}            # Get job details
PUT    /api/v1/jobs/{id}            # Update job
DELETE /api/v1/jobs/{id}            # Delete job
```

### Analysis Operations
```
POST   /api/v1/analysis              # Create analysis
GET    /api/v1/analysis              # List analyses
GET    /api/v1/analysis/{id}         # Get analysis details
DELETE /api/v1/analysis/{id}         # Delete analysis
```

## Database Schema

### CVs Table
```sql
id (UUID) - Primary Key
filename (VARCHAR)
raw_text (TEXT)
processed_text (TEXT)
skills_extracted (JSON)
created_at (TIMESTAMP)
```

### Jobs Table
```sql
id (UUID) - Primary Key
title (VARCHAR) - Indexed
description (TEXT)
skills_required (JSON)
created_at (TIMESTAMP)
```

### Analyses Table
```sql
id (UUID) - Primary Key
cv_id (UUID) - FK to CVs
job_id (UUID) - FK to Jobs (Nullable)
match_score (INTEGER 0-100)
missing_skills (JSON)
strengths (JSON)
recommendations (TEXT)
roadmap (TEXT)
created_at (TIMESTAMP)
```

## Technology Stack

- **Framework**: FastAPI 0.104.1
- **Server**: Uvicorn 0.24.0
- **Database ORM**: SQLAlchemy 2.0.23
- **Database Driver**: psycopg2-binary 2.9.9
- **Validation**: Pydantic 2.5.0
- **PDF Parsing**: pdfplumber 0.10.3
- **NLP**: spaCy 3.7.2
- **AI**: OpenAI 1.3.9
- **Async**: aiofiles 23.2.1
- **Environment**: python-dotenv 1.0.0
- **Containerization**: Docker

## Installation & Setup

### Prerequisites
- Python 3.11+
- PostgreSQL 12+
- Docker & Docker Compose (for containerized deployment)
- OpenAI API Key

### Local Development Setup

1. **Clone repository**
```bash
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your settings
```

5. **Run database migrations**
```bash
# Database is auto-created on first startup
```

6. **Start development server**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker Deployment

1. **Build and run with Docker Compose**
```bash
docker-compose up -d
```

2. **Access the application**
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

3. **View logs**
```bash
docker-compose logs -f api
```

4. **Stop services**
```bash
docker-compose down
```

## Configuration

### Environment Variables (.env)
```
DATABASE_URL=postgresql://user:password@localhost:5432/job_intelligence
OPENAI_API_KEY=sk-...
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=INFO
```

### Settings (config.py)
- Database URL
- OpenAI API key and model
- Application environment
- API configuration
- File upload limits
- Cache TTL

## API Usage Examples

### 1. Upload CV
```bash
curl -X POST "http://localhost:8000/api/v1/cv/upload" \
  -F "file=@resume.pdf"
```

### 2. Create Job
```bash
curl -X POST "http://localhost:8000/api/v1/jobs" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Senior Python Developer",
    "description": "We are looking for a senior Python developer..."
  }'
```

### 3. Perform Analysis
```bash
curl -X POST "http://localhost:8000/api/v1/analysis" \
  -H "Content-Type: application/json" \
  -d '{
    "cv_id": "550e8400-e29b-41d4-a716-446655440000",
    "job_id": "550e8400-e29b-41d4-a716-446655440001"
  }'
```

### 4. Get Analysis Results
```bash
curl "http://localhost:8000/api/v1/analysis/550e8400-e29b-41d4-a716-446655440002"
```

## Design Patterns & Best Practices

### 1. Dependency Injection
- FastAPI's `Depends()` for database sessions
- Loose coupling between services
- Easy testing and mocking

### 2. Service Layer Pattern
- Business logic separated from routes
- Reusable services across endpoints
- Clear separation of concerns

### 3. Schema Validation
- Pydantic for request/response validation
- Type safety and auto-documentation
- Clear API contracts

### 4. Error Handling
- Global exception handlers
- Proper HTTP status codes
- Detailed error messages in development

### 5. Logging
- Structured logging throughout
- Configurable log levels
- Helps with debugging and monitoring

### 6. Database Design
- UUID primary keys for scalability
- Foreign key relationships
- Indexes on frequently queried columns
- Timestamp tracking

### 7. Caching Strategy
- TTL-based cache invalidation
- Reduces API calls and costs
- Improves response times

## Performance Considerations

### Database
- Connection pooling (pool_size=10, max_overflow=20)
- Indexed frequently queried columns
- Efficient query patterns with SQLAlchemy

### PDF Processing
- Text length limits to prevent memory issues
- Streaming uploads for large files
- Temporary file cleanup

### AI Operations
- Prompt optimization for efficiency
- Token limit management
- Cache to avoid redundant calls

### Async Operations
- FastAPI's async support for I/O operations
- Non-blocking file uploads
- Efficient resource utilization

## Security Considerations

### Input Validation
- File type validation (PDF only)
- File size limits
- Text length constraints
- Pydantic validation

### Database Security
- Parameterized queries (SQLAlchemy ORM)
- Connection string in environment variables
- No hardcoded credentials

### API Security
- CORS configuration
- Error message sanitization
- No sensitive data in logs (debug mode)

## Monitoring & Logging

### Application Logs
- Request/response logging
- Error tracking
- Performance metrics
- Configurable log levels

### Health Checks
- `/health` - Service health
- `/ready` - Readiness probe
- Database connectivity checks

## Error Handling

### HTTP Status Codes
- 200: OK
- 201: Created
- 204: No Content
- 400: Bad Request
- 404: Not Found
- 413: Payload Too Large
- 500: Internal Server Error

### Exception Handlers
- File validation errors
- Database errors
- OpenAI API errors
- Generic error fallbacks

## Testing

To run tests:
```bash
pytest tests/ -v
```

## Production Deployment

### Docker Image Build
```bash
docker build -t job-intelligence-api:latest ./backend
```

### Kubernetes Deployment
- Use health check endpoints for probes
- Scale API replicas independently
- Persistent volume for database
- Network policies for security

### Environment Setup
```bash
# Set production environment
ENVIRONMENT=production
DEBUG=False
LOG_LEVEL=WARNING

# Use production database
DATABASE_URL=postgresql://prod_user:strong_password@prod_db_host:5432/job_intelligence

# Use production OpenAI API key
OPENAI_API_KEY=sk-prod-...
```

## Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## Common Issues & Solutions

### 1. PDF Extraction Issues
- Ensure pdfplumber is installed
- Check file permissions
- Verify PDF is valid and text-readable

### 2. spaCy Model Issues
```bash
python -m spacy download en_core_web_sm
```

### 3. Database Connection
- Verify PostgreSQL is running
- Check DATABASE_URL format
- Ensure database exists

### 4. OpenAI API Errors
- Verify API key is valid
- Check API quota and rate limits
- Ensure request format matches API requirements

## License

See LICENSE file

## Support

For issues and questions, please refer to the project documentation or contact the development team.
