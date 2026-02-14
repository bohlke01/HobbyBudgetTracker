# Continuous Deployment to PythonAnywhere

This document describes the continuous deployment (CD) setup for automatically deploying the Hobby Budget Tracker to PythonAnywhere whenever changes are pushed to the main branch.

## Overview

The continuous deployment system uses GitHub Actions to automatically:
1. Detect when code is pushed to the main branch
2. Reload your PythonAnywhere web application

**Important:** The GitHub Actions workflow **only reloads** the web application. You must separately configure automatic code pulling on PythonAnywhere (see Step 3 below) for a fully automated deployment.

## Prerequisites

Before enabling continuous deployment, you need:

1. **A PythonAnywhere Account** - Sign up at [www.pythonanywhere.com](https://www.pythonanywhere.com)
2. **Initial Deployment** - Follow [DEPLOYMENT.md](DEPLOYMENT.md) to set up your app on PythonAnywhere first
3. **PythonAnywhere API Token** - Get it from your [Account page](https://www.pythonanywhere.com/account/#api_token)
4. **GitHub Repository Secrets** - Admin access to configure secrets

## Setup Instructions

### Step 1: Get Your PythonAnywhere API Token

1. Log in to [PythonAnywhere](https://www.pythonanywhere.com)
2. Go to your [Account page](https://www.pythonanywhere.com/account/#api_token)
3. In the "API Token" section, click **"Create a new API token"** if you don't have one
4. Copy the token (you'll need it in the next step)

### Step 2: Configure GitHub Secrets

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"** and add the following:

   **Required Secrets:**
   
   - **Name:** `PYTHONANYWHERE_USERNAME`
     - **Value:** Your PythonAnywhere username (e.g., `john_doe`)
   
   - **Name:** `PYTHONANYWHERE_API_TOKEN`
     - **Value:** The API token you copied from PythonAnywhere

   **Optional Secret:**
   
   - **Name:** `PYTHONANYWHERE_DOMAIN`
     - **Value:** Your custom domain if different from `username.pythonanywhere.com`
     - If not set, defaults to `{username}.pythonanywhere.com`

### Step 3: Set Up Auto-Pull on PythonAnywhere

For the deployment to work properly, your PythonAnywhere application needs to pull the latest code. There are two approaches:

#### Option A: Manual Pull (Simple, but requires manual step)

After each deployment, you need to manually pull the code:
```bash
cd ~/HobbyBudgetTracker
git pull origin main
```

#### Option B: Scheduled Task (Recommended)

Set up a scheduled task on PythonAnywhere to automatically pull code:

1. Go to the **Tasks** tab on PythonAnywhere
2. Add a new scheduled task:
   - **Command:** `cd /home/yourusername/HobbyBudgetTracker && git pull origin main`
   - **Frequency:** Every hour (or your preferred interval)
   - Replace `yourusername` with your actual username

#### Option C: Add Pull Script to Reload (Advanced)

You can modify your WSGI configuration to pull before loading:

```python
import subprocess
import os

# Pull latest code
project_home = os.environ.get('PROJECT_HOME', '/home/yourusername/HobbyBudgetTracker')
try:
    subprocess.run(['git', 'pull', 'origin', 'main'], cwd=project_home, check=True)
except Exception as e:
    print(f"Git pull failed: {e}")

# ... rest of your WSGI configuration
```

**Note:** This approach adds latency to each app start, so it's not recommended for high-traffic sites.

### Step 4: Test the Deployment

1. Make a small change to your code (e.g., update README.md)
2. Commit and push to the main branch:
   ```bash
   git add .
   git commit -m "Test continuous deployment"
   git push origin main
   ```
3. Go to your repository's **Actions** tab
4. You should see a "Deploy to PythonAnywhere" workflow running
5. Wait for it to complete (usually takes less than a minute)
6. If you set up auto-pull (Option B or C above), your changes should be live
7. If using manual pull (Option A), run `git pull` on PythonAnywhere and reload

## How It Works

### GitHub Actions Workflow

The workflow (`.github/workflows/deploy-pythonanywhere.yml`) runs when:
- Code is pushed to the `main` branch
- Manually triggered via the GitHub Actions UI

The workflow performs these steps:
1. **Checkout code** - Gets the latest code from the repository (for validation)
2. **Reload Web App** - Uses the PythonAnywhere API to reload the web application
3. **Summary** - Provides deployment status in the GitHub Actions summary

**Note:** The workflow does NOT automatically pull code to PythonAnywhere. You must set up automatic code pulling separately (Step 3 above).

### Complete Deployment Flow

For a complete automated deployment:
1. **You push code** → GitHub repository updated
2. **GitHub Actions triggers** → Workflow runs
3. **PythonAnywhere pulls code** → Via scheduled task/WSGI (you set this up in Step 3)
4. **GitHub Actions reloads app** → New code becomes active

### PythonAnywhere API

The deployment uses PythonAnywhere's REST API:
- **Reload endpoint:** `POST /api/v0/user/{username}/webapps/{domain}/reload/`
- **Authentication:** Bearer token (your API token)

### Manual Deployment Script

You can also reload manually using the provided script:

```bash
# Set environment variables
export PYTHONANYWHERE_USERNAME=your_username
export PYTHONANYWHERE_API_TOKEN=your_token

# Run the deployment script
./deploy_pythonanywhere.sh
```

## Workflow File

The continuous deployment workflow is located at:
```
.github/workflows/deploy-pythonanywhere.yml
```

## Monitoring Deployments

### View Deployment History

1. Go to your repository's **Actions** tab
2. Click on "Deploy to PythonAnywhere"
3. You'll see a list of all deployment runs

### View Deployment Logs

1. Click on any deployment run
2. Click on the "deploy" job
3. Expand the steps to see detailed logs

### Check Application Status

After deployment, check your application:
1. Visit your PythonAnywhere web app URL
2. Check the **Web** tab on PythonAnywhere for any errors
3. View error logs at `/var/log/{username}.pythonanywhere.com.error.log`

## Troubleshooting

### Deployment Skipped - Secrets Not Configured

**Problem:** The workflow runs but skips deployment with a message about missing secrets.

**Solution:** Make sure you've added the required secrets (see Step 2 above).

### API Authentication Failed

**Problem:** Deployment fails with authentication errors.

**Solution:**
- Verify your API token is correct
- Generate a new API token if the old one expired
- Update the `PYTHONANYWHERE_API_TOKEN` secret in GitHub

### Reload Failed but Code Updated

**Problem:** The reload request fails, but you can manually reload and it works.

**Solution:** This is usually not critical. The code has been pulled, you just need to manually reload the app once.

### Changes Not Visible After Deployment

**Problem:** Deployment succeeds, but changes don't appear on the website.

**Solution:**
- Verify that code is being pulled on PythonAnywhere (check Step 3)
- Manually run `git pull` on PythonAnywhere to confirm
- Check the PythonAnywhere error logs for issues
- Hard refresh your browser (Ctrl+F5) to clear cache

### Domain Not Found

**Problem:** API returns 404 when trying to reload the web app.

**Solution:**
- Verify your `PYTHONANYWHERE_DOMAIN` secret is correct
- It should be in the format: `username.pythonanywhere.com`
- Check the Web tab on PythonAnywhere to confirm your domain

## Security Notes

1. **API Token:** Keep your API token secret. Never commit it to the repository.
2. **Secrets:** GitHub secrets are encrypted and only available during workflow runs.
3. **Access Control:** Only repository admins can view/edit secrets.
4. **Token Rotation:** Consider rotating your API token periodically.

## Manual Deployment

If you need to deploy manually (without pushing to main):

### Using GitHub Actions UI

1. Go to **Actions** tab
2. Click "Deploy to PythonAnywhere"
3. Click "Run workflow"
4. Select the branch and click "Run workflow"

### Using the Deployment Script

```bash
# Set environment variables
export PYTHONANYWHERE_USERNAME=your_username
export PYTHONANYWHERE_API_TOKEN=your_token

# Run the script
./deploy_pythonanywhere.sh
```

## Disabling Continuous Deployment

To temporarily disable continuous deployment:

1. Go to repository **Settings** → **Actions** → **General**
2. Disable workflow or specific workflow file
3. Or, delete/rename the workflow file `.github/workflows/deploy-pythonanywhere.yml`

## Additional Resources

- [PythonAnywhere API Documentation](https://help.pythonanywhere.com/pages/API/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Deployment Guide](DEPLOYMENT.md) - Initial setup
- [PythonAnywhere Quick Start](PYTHONANYWHERE_QUICKSTART.md) - Quick reference

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review GitHub Actions logs
3. Check PythonAnywhere error logs
4. Open an issue in the repository

## Next Steps

After setting up continuous deployment:
1. Consider setting up deployment environments (staging, production)
2. Add automated tests before deployment
3. Implement deployment notifications (Slack, email, etc.)
4. Set up monitoring and alerting for your application
