#!/bin/bash
# Database Setup Script for Job Intelligence Platform

set -e

echo "=========================================="
echo "Job Intelligence Platform - Database Setup"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo -e "${RED}✗ PostgreSQL is not installed${NC}"
    echo "Install it with: sudo apt-get install postgresql postgresql-contrib"
    exit 1
fi

echo -e "${GREEN}✓ PostgreSQL is installed${NC}"

# Check if PostgreSQL service is running
if ! sudo systemctl is-active --quiet postgresql; then
    echo -e "${YELLOW}⚠ PostgreSQL service is not running${NC}"
    echo "Starting PostgreSQL..."
    sudo systemctl start postgresql
fi

echo -e "${GREEN}✓ PostgreSQL service is running${NC}"
echo ""

# Read database configuration
read -p "Enter database user (default: user): " DB_USER
DB_USER=${DB_USER:-user}

read -sp "Enter database password: " DB_PASSWORD
echo ""

DB_NAME="job_intelligence"
DB_HOST="localhost"

echo ""
echo "Configuration:"
echo "  Database: $DB_NAME"
echo "  User: $DB_USER"
echo "  Host: $DB_HOST"
echo ""

# Create user if it doesn't exist
echo "Creating database user..."
if sudo -u postgres psql -tc "SELECT 1 FROM pg_user WHERE usename = '$DB_USER'" | grep -q 1; then
    echo -e "${YELLOW}⚠ User '$DB_USER' already exists${NC}"
else
    sudo -u postgres psql -c "CREATE USER \"$DB_USER\" WITH PASSWORD '$DB_PASSWORD';"
    echo -e "${GREEN}✓ User '$DB_USER' created${NC}"
fi

# Create database if it doesn't exist
echo "Creating database..."
if sudo -u postgres psql -tc "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME'" | grep -q 1; then
    echo -e "${YELLOW}⚠ Database '$DB_NAME' already exists${NC}"
    sudo -u postgres psql -c "ALTER DATABASE $DB_NAME OWNER TO \"$DB_USER\";"
else
    sudo -u postgres createdb "$DB_NAME" -O "$DB_USER"
    echo -e "${GREEN}✓ Database '$DB_NAME' created${NC}"
fi

# Grant privileges
echo "Granting privileges..."
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO \"$DB_USER\";"
sudo -u postgres psql -d "$DB_NAME" -c "GRANT ALL PRIVILEGES ON SCHEMA public TO \"$DB_USER\";"
echo -e "${GREEN}✓ Privileges granted${NC}"

echo ""
echo "Database setup complete!"
echo ""
echo "Update your .env file with:"
echo "  DATABASE_URL=postgresql://$DB_USER:$DB_PASSWORD@$DB_HOST:5432/$DB_NAME"
echo ""
echo "Test connection with:"
echo "  psql -h $DB_HOST -U $DB_USER -d $DB_NAME"
