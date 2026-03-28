#!/usr/bin/env bash

# ============================================================
# Job Intelligence Platform - Deployment Verification Script
# ============================================================
# This script verifies that everything is ready for deployment

echo "🔍 Verifying Job Intelligence Platform Deployment Readiness..."
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counter for checks
PASSED=0
FAILED=0

# Function to check file existence
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✅${NC} $2"
        ((PASSED++))
    else
        echo -e "${RED}❌${NC} $2 - File not found: $1"
        ((FAILED++))
    fi
}

# Function to check directory existence
check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✅${NC} $2"
        ((PASSED++))
    else
        echo -e "${RED}❌${NC} $2 - Directory not found: $1"
        ((FAILED++))
    fi
}

# Function to check if command exists
check_command() {
    if command -v "$1" &> /dev/null; then
        echo -e "${GREEN}✅${NC} $2"
        ((PASSED++))
    else
        echo -e "${YELLOW}⚠️${NC} $2 - Install with: $3"
        ((FAILED++))
    fi
}

echo "📦 Backend Files..."
check_file "backend/Dockerfile" "Docker configuration"
check_file "backend/.dockerignore" "Docker ignore file"
check_file "backend/docker-compose.prod.yml" "Production Docker Compose"
check_file "backend/startup.sh" "Azure startup script"
check_file "backend/.env.example" "Environment template"
check_file "backend/requirements.txt" "Python dependencies"
check_file "backend/core/config.py" "Configuration module"

echo ""
echo "🌐 Frontend Files..."
check_file "frontend/vercel.json" "Vercel configuration"
check_file "frontend/.env.example" "Frontend environment template"
check_file "frontend/package.json" "NPM dependencies"
check_file "frontend/vite.config.js" "Vite configuration"
check_file "frontend/src/services/api.js" "API service"

echo ""
echo "📚 Documentation..."
check_file "DEPLOYMENT.md" "Deployment guide"
check_file "DEPLOYMENT_CHECKLIST.md" "Pre-deployment checklist"
check_file "DEPLOYMENT_READY.md" "Deployment readiness summary"

echo ""
echo "📁 Directory Structure..."
check_dir "backend/app" "Backend app directory"
check_dir "backend/models" "Database models"
check_dir "backend/schemas" "Pydantic schemas"
check_dir "backend/services" "Business logic services"
check_dir "backend/core" "Core configuration"
check_dir "frontend/src" "Frontend source"
check_dir "frontend/src/components" "Frontend components"

echo ""
echo "🔧 Environment Variables..."

# Check for sensitive data in code
if grep -r "sk-" backend/ 2>/dev/null | grep -v ".env" > /dev/null; then
    echo -e "${RED}❌${NC} Hardcoded OpenAI keys found in code"
    ((FAILED++))
else
    echo -e "${GREEN}✅${NC} No hardcoded API keys in code"
    ((PASSED++))
fi

if grep -r "password" backend/ 2>/dev/null | grep -v ".env" | grep -v "example" > /dev/null; then
    echo -e "${YELLOW}⚠️${NC} Check for hardcoded passwords"
    ((FAILED++))
else
    echo -e "${GREEN}✅${NC} No hardcoded passwords in code"
    ((PASSED++))
fi

echo ""
echo "🛠️ System Tools..."
check_command "docker" "Docker installed" "Visit: https://docs.docker.com/get-docker/"
check_command "git" "Git installed" "Visit: https://git-scm.com/downloads"
check_command "node" "Node.js installed" "Visit: https://nodejs.org/"

echo ""
echo "════════════════════════════════════════════"
echo "📊 RESULTS"
echo "════════════════════════════════════════════"
echo -e "✅ Passed: ${GREEN}$PASSED${NC}"
echo -e "❌ Failed: ${RED}$FAILED${NC}"
echo "════════════════════════════════════════════"

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✨ Everything is ready for deployment! ✨${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Review DEPLOYMENT.md for detailed instructions"
    echo "2. Set up Azure resources"
    echo "3. Configure environment variables"
    echo "4. Build and push Docker image"
    echo "5. Deploy frontend to Vercel"
    exit 0
else
    echo -e "${RED}⚠️ Please address the above issues before deploying${NC}"
    exit 1
fi
