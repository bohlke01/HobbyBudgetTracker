#!/bin/bash
#
# Deployment script for PythonAnywhere
# 
# This script automates the deployment process to PythonAnywhere.
# It can be run locally or used by CI/CD pipelines.
#
# Usage:
#   ./deploy_pythonanywhere.sh
#
# Required environment variables:
#   PYTHONANYWHERE_USERNAME  - Your PythonAnywhere username
#   PYTHONANYWHERE_API_TOKEN - Your PythonAnywhere API token
#
# Optional environment variables:
#   PYTHONANYWHERE_DOMAIN    - Your domain (defaults to username.pythonanywhere.com)
#

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check required environment variables
if [ -z "$PYTHONANYWHERE_USERNAME" ]; then
    echo -e "${RED}Error: PYTHONANYWHERE_USERNAME environment variable is not set${NC}"
    echo "Please set your PythonAnywhere username:"
    echo "  export PYTHONANYWHERE_USERNAME=your_username"
    exit 1
fi

if [ -z "$PYTHONANYWHERE_API_TOKEN" ]; then
    echo -e "${RED}Error: PYTHONANYWHERE_API_TOKEN environment variable is not set${NC}"
    echo "Please get your API token from: https://www.pythonanywhere.com/account/#api_token"
    echo "Then set it with:"
    echo "  export PYTHONANYWHERE_API_TOKEN=your_token"
    exit 1
fi

# Set domain default if not provided
DOMAIN="${PYTHONANYWHERE_DOMAIN:-${PYTHONANYWHERE_USERNAME}.pythonanywhere.com}"

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║         PythonAnywhere Deployment Script                  ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}Target:${NC} https://${DOMAIN}"
echo -e "${BLUE}Username:${NC} ${PYTHONANYWHERE_USERNAME}"
echo ""

# Function to make API calls
api_call() {
    local method=$1
    local endpoint=$2
    local data=$3
    
    if [ -n "$data" ]; then
        curl -s -w "\n%{http_code}" -X "$method" \
            -H "Authorization: Token ${PYTHONANYWHERE_API_TOKEN}" \
            -H "Content-Type: application/json" \
            -d "$data" \
            "https://www.pythonanywhere.com/api/v0${endpoint}"
    else
        curl -s -w "\n%{http_code}" -X "$method" \
            -H "Authorization: Token ${PYTHONANYWHERE_API_TOKEN}" \
            "https://www.pythonanywhere.com/api/v0${endpoint}"
    fi
}

# Note: This script reloads the web application but does not pull code
# You need to set up automatic code pulling on PythonAnywhere separately
# See CONTINUOUS_DEPLOYMENT.md Step 3 for setup options:
#   - Option A: Manual git pull after deployment
#   - Option B: Scheduled task to auto-pull
#   - Option C: Git pull in WSGI configuration

echo -e "${YELLOW}ℹ️  This script will reload your web application.${NC}"
echo -e "${YELLOW}   Make sure code updates are handled separately (see CONTINUOUS_DEPLOYMENT.md)${NC}"
echo ""

# Step 1: Reload web application
echo -e "${YELLOW}🔄 Reloading web application...${NC}"

RELOAD_RESPONSE=$(api_call POST "/user/${PYTHONANYWHERE_USERNAME}/webapps/${DOMAIN}/reload/")
HTTP_CODE=$(echo "$RELOAD_RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$RELOAD_RESPONSE" | head -n-1)

if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✅ Web application reloaded successfully!${NC}"
else
    echo -e "${YELLOW}⚠️  Reload returned status code: $HTTP_CODE${NC}"
    if [ -n "$RESPONSE_BODY" ]; then
        echo "Response: $RESPONSE_BODY"
    fi
fi

# Step 2: Check web app status
echo -e "${YELLOW}🔍 Checking web application status...${NC}"

STATUS_RESPONSE=$(api_call GET "/user/${PYTHONANYWHERE_USERNAME}/webapps/${DOMAIN}/")
HTTP_CODE=$(echo "$STATUS_RESPONSE" | tail -n1)

if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✅ Web application is running${NC}"
else
    echo -e "${RED}⚠️  Could not verify web application status (HTTP $HTTP_CODE)${NC}"
fi

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║            Reload Complete!                                ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}🌐 Your application:${NC} https://${DOMAIN}"
echo ""
echo -e "${YELLOW}⚠️  Important:${NC} This script only reloaded the web app."
echo ""
echo -e "${YELLOW}To update code:${NC}"
echo "  1. SSH/Console: cd ~/HobbyBudgetTracker && git pull origin main"
echo "  2. Or set up auto-pull (see CONTINUOUS_DEPLOYMENT.md Step 3)"
echo ""
echo -e "${YELLOW}Recommended setup for full automation:${NC}"
echo "  - Use a scheduled task on PythonAnywhere to run 'git pull' hourly"
echo "  - See CONTINUOUS_DEPLOYMENT.md for detailed instructions"
echo ""
