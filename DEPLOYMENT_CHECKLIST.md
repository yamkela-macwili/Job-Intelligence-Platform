# Pre-Deployment Checklist

> Complete checklist before deploying to Azure (Backend) + Vercel (Frontend)

---

## 🔧 Backend Configuration

### Environment Setup
- [ ] `backend/.env.example` updated with Azure PostgreSQL format
- [ ] `backend/core/config.py` has DEBUG=False as default
- [ ] Azure credentials are configured locally (`az login`)
- [ ] Azure CLI is installed and working

### Docker Configuration
- [ ] `backend/Dockerfile` is production-ready
- [ ] `backend/.dockerignore` excludes unnecessary files
- [ ] `backend/docker-compose.prod.yml` created
- [ ] `backend/startup.sh` script created

### Code Quality
- [ ] No hardcoded credentials in code
- [ ] All imports are available in `requirements.txt`
- [ ] API endpoints are tested locally
- [ ] Error handling is comprehensive
- [ ] Logging is configured for production

### Database
- [ ] Database migration scripts are ready
- [ ] PostgreSQL connection string format verified
- [ ] SSL/TLS mode enabled for PostgreSQL
- [ ] Database backup strategy planned

---

## 🌐 Frontend Configuration

### Environment Setup
- [ ] `frontend/.env.example` created
- [ ] `frontend/vercel.json` created with proper config
- [ ] `vite.config.js` is optimized
- [ ] `package.json` build script is correct

### API Integration
- [ ] `src/services/api.js` uses `VITE_API_BASE_URL` environment variable
- [ ] API base URL points to Azure backend
- [ ] CORS configuration allows frontend domain
- [ ] API endpoints are tested with backend

### Code Quality
- [ ] No hardcoded URLs in code
- [ ] All dependencies are in `package.json`
- [ ] Build completes without errors: `npm run build`
- [ ] All pages load and function correctly
- [ ] No console errors or warnings

### Build & Optimization
- [ ] Build output is generated: `npm run build`
- [ ] Output directory is `dist`
- [ ] Source maps are generated for debugging
- [ ] Asset optimization is enabled

---

## ☁️ Azure Setup

### Prerequisite Resources
- [ ] Azure subscription is active
- [ ] Resource group created (e.g., `job-intelligence-rg`)
- [ ] PostgreSQL server created and running
- [ ] App Service plan created
- [ ] Web App created
- [ ] Container registry created (optional)

### Environment Variables in Azure
- [ ] `DATABASE_URL` set correctly
- [ ] `AZURE_AI_API_KEY` configured
- [ ] `AZURE_AI_ENDPOINT` configured
- [ ] `AZURE_AI_MODEL_DEPLOYMENT_NAME` set to `gpt-4o`
- [ ] `ENVIRONMENT` set to `production`
- [ ] `DEBUG` set to `False`
- [ ] `LOG_LEVEL` set to `INFO`

### Security
- [ ] SSL/TLS certificate is valid
- [ ] PostgreSQL firewall rules configured
- [ ] Azure Key Vault secrets created (optional)
- [ ] Managed identities enabled (optional)

### Monitoring
- [ ] Application Insights enabled
- [ ] Log retention configured
- [ ] Alerts set up for errors
- [ ] Performance monitoring enabled

---

## 🚀 Vercel Setup

### Project Configuration
- [ ] GitHub repository is public or properly shared
- [ ] Vercel account is created
- [ ] Project is connected to Vercel
- [ ] Build settings configured:
  - Build Command: `npm run build`
  - Output Directory: `dist`

### Environment Variables in Vercel
- [ ] `VITE_API_BASE_URL` set to Azure App Service URL
- [ ] No sensitive data in environment variables
- [ ] Environment variables are marked as secret if needed

### Deployment Settings
- [ ] Auto-deployments enabled for main branch
- [ ] Preview deployments enabled for PRs
- [ ] Root directory set to `frontend`

---

## 🧪 Testing

### Backend Testing
- [ ] `GET /health` returns 200 OK
- [ ] `GET /ready` returns 200 OK
- [ ] `POST /api/v1/cv/upload` accepts PDF files
- [ ] `POST /api/v1/jobs` creates job entries
- [ ] `POST /api/v1/analysis` generates analysis
- [ ] `GET /api/v1/analysis/{id}` retrieves results
- [ ] Error handling returns proper status codes
- [ ] API documentation available at `/docs`

### Frontend Testing
- [ ] Page loads without errors
- [ ] Navigation works correctly
- [ ] File upload form displays
- [ ] API calls to backend succeed
- [ ] Results display with correct data
- [ ] Responsive design works on mobile
- [ ] No console errors or warnings

### Integration Testing
- [ ] Frontend can upload CV to backend
- [ ] Backend extracts CV data correctly
- [ ] Analysis results return to frontend
- [ ] Frontend displays results properly
- [ ] Roadmap displays with correct formatting
- [ ] End-to-end workflow completes successfully

---

## 📝 Documentation

- [ ] `DEPLOYMENT.md` created with full instructions
- [ ] `README.md` updated with deployment info
- [ ] `.env.example` files created for both backend and frontend
- [ ] API documentation is accessible
- [ ] Troubleshooting guide is complete

---

## 🔐 Security Verification

- [ ] No `.env` files committed to git
- [ ] `.gitignore` includes sensitive files
- [ ] API keys not exposed in logs
- [ ] CORS is properly configured
- [ ] Input validation is implemented
- [ ] SQL injection prevention (ORM used)
- [ ] HTTPS enforced in production
- [ ] Rate limiting configured (optional)

---

## 📊 Performance

- [ ] Database connection pooling enabled
- [ ] Query optimization implemented
- [ ] Frontend assets are minified
- [ ] Images are optimized
- [ ] Caching headers configured
- [ ] CDN enabled for static assets (Vercel)
- [ ] Response times are acceptable (<500ms)

---

## ✅ Final Verification

### Before Pushing to Production
- [ ] All tests pass locally
- [ ] No sensitive data in repository
- [ ] Environment variables are set in cloud platforms
- [ ] Backup strategy is in place
- [ ] Monitoring and alerts are configured
- [ ] Team is aware of deployment

### After Initial Deployment
- [ ] Monitor logs for errors
- [ ] Test all user workflows
- [ ] Check performance metrics
- [ ] Verify monitoring is working
- [ ] Document any issues found

---

## 📞 Deployment Support

- **Backend Issues**: Check Azure Portal → Application Insights
- **Frontend Issues**: Check Vercel Dashboard → Deployments
- **Database Issues**: Check Azure Portal → PostgreSQL Server
- **API Issues**: Check backend logs and API documentation

---

**Deployment Date:** _______________  
**Deployed By:** _______________  
**Verified By:** _______________  

**Status:** Ready for Production ✅

---

**Last Updated:** March 28, 2026
