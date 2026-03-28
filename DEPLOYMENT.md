# Deployment Guide - Job Intelligence Platform

> Complete deployment guide for Azure Backend + Vercel Frontend

---

## 📋 Prerequisites

### Backend (Azure)
- Azure subscription with:
  - Azure App Service plan
  - Azure Database for PostgreSQL
  - Azure OpenAI API access
- Docker installed locally
- Azure CLI installed (`az login` configured)

### Frontend (Vercel)
- Vercel account
- GitHub account with repository access
- Node.js 18+ installed

---

## 🚀 Backend Deployment (Azure App Service)

### Step 1: Prepare Azure Resources

```bash
# 1. Create Resource Group
az group create --name job-intelligence-rg --location eastus

# 2. Create PostgreSQL Server
az postgres flexible-server create \
  --resource-group job-intelligence-rg \
  --name job-intel-db \
  --admin-user dbadmin \
  --admin-password <strong-password> \
  --database-name job_intelligence

# 3. Create App Service Plan
az appservice plan create \
  --name job-intel-plan \
  --resource-group job-intelligence-rg \
  --sku B2 \
  --is-linux

# 4. Create Web App
az webapp create \
  --resource-group job-intelligence-rg \
  --plan job-intel-plan \
  --name job-intel-api \
  --runtime "PYTHON:3.11"
```

### Step 2: Configure Environment Variables in Azure

In Azure Portal or CLI, set these Application Settings:

```bash
az webapp config appsettings set \
  --name job-intel-api \
  --resource-group job-intelligence-rg \
  --settings \
    DATABASE_URL="postgresql://dbadmin:password@job-intel-db.postgres.database.azure.com:5432/job_intelligence?sslmode=require" \
    AZURE_AI_API_KEY="your-azure-openai-api-key" \
    AZURE_AI_ENDPOINT="https://your-resource.openai.azure.com/" \
    AZURE_AI_MODEL_DEPLOYMENT_NAME="gpt-4o" \
    ENVIRONMENT="production" \
    DEBUG="False" \
    LOG_LEVEL="INFO"
```

### Step 3: Deploy Backend via Docker

```bash
# 1. Navigate to backend directory
cd backend

# 2. Create Azure Container Registry (optional but recommended)
az acr create --resource-group job-intelligence-rg --name jobintelacr --sku Basic

# 3. Build and push Docker image
az acr build --registry jobintelacr --image job-intel-api:latest .

# 4. OR push to Docker Hub
docker build -t yourusername/job-intel-api:latest .
docker push yourusername/job-intel-api:latest

# 5. Configure Web App to use Docker image
az webapp config container set \
  --name job-intel-api \
  --resource-group job-intelligence-rg \
  --docker-custom-image-name yourusername/job-intel-api:latest \
  --docker-registry-server-url https://index.docker.io \
  --docker-registry-server-user <username> \
  --docker-registry-server-password <password>

# 6. Start the app
az webapp start --name job-intel-api --resource-group job-intelligence-rg
```

### Step 4: Verify Backend Deployment

```bash
# Check health endpoint
curl https://job-intel-api.azurewebsites.net/health

# Check API docs
https://job-intel-api.azurewebsites.net/docs
```

---

## 🌐 Frontend Deployment (Vercel)

### Step 1: Prepare Frontend for Production

```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Install dependencies
npm install

# 3. Create .env.production.local (NOT .env.local)
# In Vercel dashboard environment variables instead
```

### Step 2: Deploy to Vercel

#### Option A: Via Vercel CLI (Recommended)

```bash
# 1. Install Vercel CLI
npm install -g vercel

# 2. Login to Vercel
vercel login

# 3. Deploy
vercel

# 4. Set environment variable during deploy
# When asked, configure:
# VITE_API_BASE_URL = https://job-intel-api.azurewebsites.net
```

#### Option B: Via GitHub (Recommended for CI/CD)

1. Push code to GitHub repository
2. Go to [Vercel Dashboard](https://vercel.com/dashboard)
3. Click "Add New Project"
4. Import your GitHub repository
5. Configure project:
   - Framework: Vite
   - Build Command: `npm run build`
   - Output Directory: `dist`
6. Add Environment Variables:
   - Key: `VITE_API_BASE_URL`
   - Value: `https://job-intel-api.azurewebsites.net`
7. Click "Deploy"

### Step 3: Verify Frontend Deployment

```bash
# Frontend will be available at:
https://your-project-name.vercel.app

# Verify API connectivity:
# 1. Open browser dev console
# 2. Check that API requests go to Azure backend
# 3. Test upload CV functionality
```

---

## 🔒 Security Configuration

### Backend (Azure)

```bash
# 1. Enable HTTPS (automatic with Azure App Service)
# 2. Set firewall rules for PostgreSQL
az postgres flexible-server firewall-rule create \
  --name azure-services \
  --resource-group job-intelligence-rg \
  --server-name job-intel-db \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0

# 3. Enable application insights for monitoring
az monitor app-insights component create \
  --app job-intel-api \
  --location eastus \
  --resource-group job-intelligence-rg
```

### Frontend (Vercel)

```bash
# Environment variables are automatically encrypted in Vercel
# Only expose non-sensitive information
# Never commit .env files to git
```

---

## 📊 Monitoring & Logging

### Azure Backend

```bash
# View application logs
az webapp log tail --name job-intel-api --resource-group job-intelligence-rg

# View Application Insights
# Portal → App Service → Application Insights

# Check health status
curl https://job-intel-api.azurewebsites.net/health
curl https://job-intel-api.azurewebsites.net/ready
```

### Vercel Frontend

- Logs available in Vercel Dashboard → Project → Deployments → Logs
- Real User Monitoring (RUM) available in Analytics

---

## 🚨 Troubleshooting

### Backend Issues

**502 Bad Gateway:**
- Check Application Insights logs
- Verify environment variables are set correctly
- Check PostgreSQL connectivity

**API endpoints return 404:**
- Verify backend deployed successfully
- Check health endpoint: `/health`

**Database connection errors:**
- Verify DATABASE_URL format
- Check PostgreSQL firewall rules
- Ensure SSL mode is enabled

### Frontend Issues

**API calls failing:**
- Check VITE_API_BASE_URL in Vercel environment variables
- Check browser console for CORS errors
- Verify backend is running

**Build failures on Vercel:**
- Check build logs in Vercel dashboard
- Ensure dependencies are listed in package.json
- Verify vite.config.js is correct

---

## 📈 Performance Optimization

### Backend
- Connection pooling configured (10 connections)
- Response caching enabled (24 hours)
- Compression enabled
- Request logging in production mode

### Frontend
- Code splitting enabled
- Lazy loading for components
- Image optimization
- Static asset caching (1 year)
- CSS minification enabled

---

## 🔄 Continuous Deployment

### GitHub Actions (Optional)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Azure

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Login to Azure
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
      
      - name: Build Docker image
        run: docker build backend -t jobintelapi:latest
      
      - name: Push to container registry
        run: az acr build --registry jobintelacr --image job-intel-api:latest backend/
      
      - name: Deploy to App Service
        uses: azure/webapps-deploy@v2
        with:
          app-name: job-intel-api
```

---

## ✅ Post-Deployment Checklist

- [ ] Backend health check passes (`/health`, `/ready`)
- [ ] Frontend loads successfully
- [ ] API endpoints are accessible from frontend
- [ ] CV upload functionality works
- [ ] Analysis generation works
- [ ] Results display correctly
- [ ] No 404 or 500 errors in browser console
- [ ] Logs are being collected
- [ ] Monitoring is enabled
- [ ] Database backups are configured
- [ ] SSL/TLS certificates are valid
- [ ] CORS is properly configured
- [ ] Environment variables are secured
- [ ] API keys are not exposed

---

## 📞 Support

For issues or questions:
1. Check Azure Portal → Application Insights
2. Check Vercel Dashboard → Deployments
3. Review logs in both platforms
4. Consult README.md for development setup

---

**Last Updated:** March 28, 2026  
**Version:** 1.0.0  
**Status:** Production Ready ✅
