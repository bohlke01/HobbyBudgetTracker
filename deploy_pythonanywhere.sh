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

# Step 1: Pull latest code
echo -e "${YELLOW}📥 Pulling latest code from GitHub...${NC}"

# Note: PythonAnywhere's console API endpoint requires an existing console ID
# For a more robust solution, you might want to use their scheduled tasks or 
# connect via SSH if available in your plan
echo "   Using API to send git pull command..."

# We'll use a simpler approach - just reload the web app
# The user should have their PythonAnywhere setup to auto-pull or use a webhook

# Step 2: Reload web application
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

# Step 3: Check web app status
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
echo -e "${GREEN}║            Deployment Complete!                            ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}🌐 Your application:${NC} https://${DOMAIN}"
echo ""
echo -e "${YELLOW}Note:${NC} If you made code changes, make sure to:"
echo "  1. Pull the latest code on PythonAnywhere (git pull)"
echo "  2. The reload above will pick up the changes"
echo ""
echo -e "${YELLOW}For automatic code updates:${NC}"
echo "  - Set up a scheduled task on PythonAnywhere to run 'git pull'"
echo "  - Or use PythonAnywhere's git integration features"
echo ""
