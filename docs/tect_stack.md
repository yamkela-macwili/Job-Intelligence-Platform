
# TECH STACK DOCUMENTATION

---

## 1.1 System Architecture

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

## 1.2 Frontend Layer

### Technologies

* React (Vite)
* TailwindCSS
* Framer Motion

### Responsibilities

* User interaction
* API communication
* Data visualization
* UI rendering

### Deployment

* Hosted on **Vercel**

### Rationale

* Fast builds and deployments
* Global CDN performance
* Seamless Git integration

---

## 1.3 Backend Layer

### Technologies

* FastAPI (Python)

### Responsibilities

* API endpoints
* Request validation
* Service orchestration
* Response formatting

### Key Advantages

* Async support for AI calls
* Automatic API docs (`/docs`)
* Strong typing via Pydantic

---

## 1.4 AI & NLP Layer

### Technologies

* OpenAI API (LLM)
* spaCy (NLP)
* Custom scoring logic

---

### Responsibilities

#### OpenAI (LLM)

* CV-job semantic comparison
* Suggestion generation
* Roadmap creation

#### spaCy

* Skill extraction
* Entity recognition
* Text preprocessing

---

### Design Strategy

Hybrid approach:

* **LLM for reasoning**
* **spaCy for structure**

---

## 1.5 File Processing Layer

### Technology

* pdfplumber

### Responsibilities

* Extract text from CV PDFs
* Preserve structure where possible

---

## 1.6 Database Layer

### Technologies

* PostgreSQL
* SQLAlchemy (ORM)

---

### Responsibilities

* Store CV data
* Store analysis results
* Enable caching of AI outputs

---

### Why Database Without Authentication?

* Avoid recomputation of AI results
* Improve performance
* Enable session-based tracking
* Support future scalability

---

## 1.7 Deployment Architecture

### Backend

* Azure App Service

### Database

* Azure Database for PostgreSQL

### Frontend

* Vercel

---

## 1.8 Security Considerations

* Environment variables for secrets
* Secure file handling
* Input validation
* API key protection

---
