# Production Deployment Guide

## Job Intelligence Platform - Backend

This guide covers deployment of the FastAPI backend to production environments.

### Prerequisites

- Docker & Docker Compose
- PostgreSQL 13+ or use container
- OpenAI API key
- Python 3.11+ (for local development)

---

## Local Development Setup

### 1. Clone Repository

```bash
git clone <repository-url>
cd Job-Intelligence-Platform
```

### 2. Environment Configuration

Create `.env` file in project root:

```env
# Database
DB_USER=jobuser
DB_PASSWORD=your_secure_password
DB_NAME=job_intelligence

# OpenAI
OPENAI_API_KEY=sk-your-api-key-here

# Application
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=INFO
```

### 3. Start Services with Docker Compose

```bash
cd backend
docker-compose up -d
```

This will:
- Start PostgreSQL database
- Build API image
- Start FastAPI server on http://localhost:8000

### 4. Verify Installation

```bash
# Check health endpoint
curl http://localhost:8000/health

# View API documentation
# Open: http://localhost:8000/docs
```

---

## Production Deployment

### 1. Environment Configuration

Create `.env` for production:

```env
# Database
DB_USER=prod_user
DB_PASSWORD=$(openssl rand -base64 32)
DB_NAME=job_intelligence_prod

# OpenAI
OPENAI_API_KEY=sk-your-production-key

# Application
ENVIRONMENT=production
DEBUG=False
LOG_LEVEL=WARNING
```

### 2. Docker Build

```bash
cd backend
docker build -t job-intelligence-api:latest .
```

### 3. Push to Registry

```bash
# Example: Docker Hub
docker tag job-intelligence-api:latest username/job-intelligence-api:latest
docker push username/job-intelligence-api:latest
```

### 4. Deploy to Kubernetes

Create `k8s-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: job-intelligence-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: job-intelligence-api
  template:
    metadata:
      labels:
        app: job-intelligence-api
    spec:
      containers:
      - name: api
        image: username/job-intelligence-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secrets
              key: connection-string
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: openai-secrets
              key: api-key
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 10
```

Deploy:

```bash
kubectl apply -f k8s-deployment.yaml
```

### 5. Deploy to AWS ECS

Create `ecs-task-definition.json`:

```json
{
  "family": "job-intelligence-api",
  "containerDefinitions": [
    {
      "name": "api",
      "image": "username/job-intelligence-api:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "hostPort": 8000
        }
      ],
      "environment": [
        {
          "name": "ENVIRONMENT",
          "value": "production"
        }
      ],
      "secrets": [
        {
          "name": "DATABASE_URL",
          "valueFrom": "arn:aws:secretsmanager:region:account:secret:job-intelligence-db"
        },
        {
          "name": "OPENAI_API_KEY",
          "valueFrom": "arn:aws:secretsmanager:region:account:secret:openai-key"
        }
      ]
    }
  ],
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "networkMode": "awsvpc"
}
```

Register task definition:

```bash
aws ecs register-task-definition --cli-input-json file://ecs-task-definition.json
```

### 6. Deploy to Heroku

```bash
# Login to Heroku
heroku login

# Create app
heroku create job-intelligence-api

# Add PostgreSQL
heroku addons:create heroku-postgresql:standard-0 -a job-intelligence-api

# Set environment variables
heroku config:set OPENAI_API_KEY=sk-your-key -a job-intelligence-api
heroku config:set ENVIRONMENT=production -a job-intelligence-api
heroku config:set DEBUG=False -a job-intelligence-api

# Deploy
git push heroku main
```

---

## Database Migrations

### Using Alembic (Recommended)

```bash
# Install Alembic
pip install alembic

# Initialize migrations
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Initial schema"

# Apply migration
alembic upgrade head
```

### Manual SQL

```sql
-- Connect to database
psql -U jobuser -d job_intelligence

-- Create tables
CREATE TABLE cvs (
    id UUID PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    raw_text TEXT NOT NULL,
    processed_text TEXT,
    skills_extracted TEXT DEFAULT '[]',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE jobs (
    id UUID PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    skills_required TEXT DEFAULT '[]',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE analyses (
    id UUID PRIMARY KEY,
    cv_id UUID REFERENCES cvs(id),
    job_id UUID REFERENCES jobs(id),
    match_score INTEGER DEFAULT 0,
    missing_skills TEXT DEFAULT '[]',
    strengths TEXT DEFAULT '[]',
    recommendations TEXT,
    roadmap TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## Monitoring & Logging

### Health Checks

```bash
# Continuous health monitoring
watch curl -s http://localhost:8000/health | jq
```

### View Logs

```bash
# Docker logs
docker logs -f job_intelligence_api

# Docker Compose logs
docker-compose logs -f api
```

### Performance Monitoring

Add monitoring stack (`prometheus`, `grafana`):

```yaml
monitoring:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
  
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

---

## Scaling

### Horizontal Scaling (Multiple Instances)

```bash
# Scale Docker Compose
docker-compose up --scale api=3
```

### Load Balancing with Nginx

```nginx
upstream backend {
    server api-1:8000;
    server api-2:8000;
    server api-3:8000;
}

server {
    listen 80;
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## Backup & Recovery

### Database Backup

```bash
# Backup PostgreSQL
pg_dump -U jobuser job_intelligence > backup.sql

# Docker container backup
docker exec job_intelligence_db pg_dump -U jobuser job_intelligence > backup.sql
```

### Restore from Backup

```bash
# Restore PostgreSQL
psql -U jobuser job_intelligence < backup.sql

# Docker container restore
cat backup.sql | docker exec -i job_intelligence_db psql -U jobuser job_intelligence
```

---

## Troubleshooting

### Database Connection Issues

```bash
# Test connection
psql -h localhost -U jobuser -d job_intelligence

# Check PostgreSQL status
docker ps | grep postgres
```

### API Not Responding

```bash
# Check logs
docker logs job_intelligence_api

# Restart container
docker-compose restart api
```

### High Memory Usage

```bash
# Check container stats
docker stats job_intelligence_api

# Adjust limits in docker-compose.yml
# Add deploy section:
# deploy:
#   resources:
#     limits:
#       memory: 2G
```

---

## Security Best Practices

1. **Secrets Management**
   - Use environment variables for sensitive data
   - Consider HashiCorp Vault or AWS Secrets Manager

2. **Database Security**
   - Use strong passwords
   - Enable SSL connections
   - Restrict network access

3. **API Security**
   - Enable HTTPS
   - Implement rate limiting
   - Use API keys for authentication

4. **CORS Configuration**
   - Restrict allowed origins in production
   - Review CORS settings in `app/main.py`

---

## Support & Documentation

- API Documentation: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- GitHub Issues: [project-repo]/issues
