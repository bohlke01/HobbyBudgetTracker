# Deploying Hobby Budget Tracker on PythonAnywhere

This guide will walk you through the steps to deploy the Hobby Budget Tracker web application on PythonAnywhere.

> **💡 Want automated deployments?** After completing initial setup, see [CONTINUOUS_DEPLOYMENT.md](CONTINUOUS_DEPLOYMENT.md) to enable continuous deployment via GitHub Actions.

## Prerequisites

- A PythonAnywhere account (free tier is sufficient)
- Basic familiarity with the command line

## Step-by-Step Deployment Guide

### 1. Sign Up for PythonAnywhere

1. Go to [www.pythonanywhere.com](https://www.pythonanywhere.com)
2. Create a free account (or log in if you already have one)
3. Verify your email address

### 2. Clone the Repository

1. Once logged in, go to the **Consoles** tab
2. Start a **Bash console**
3. Clone your repository:
   ```bash
   git clone https://github.com/bohlke01/HobbyBudgetTracker.git
   cd HobbyBudgetTracker
   ```

### 3. Set Up a Virtual Environment

1. Create a virtual environment with Python 3.10 (or your preferred version):
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 hobby-budget-env
   ```

2. The virtual environment will be automatically activated. Install the dependencies:
   ```bash
   pip install -e .
   ```

   This will install Flask and set up the package.

3. Verify the installation:
   ```bash
   pip list
   ```
   You should see Flask and hobby-budget-tracker in the list.

### 4. Configure the Web App

1. Go to the **Web** tab in your PythonAnywhere dashboard
2. Click **Add a new web app**
3. Choose **Manual configuration** (not the Flask wizard, as we have our own setup)
4. Select **Python 3.10** (or the version you used for your virtualenv)
5. Click **Next** and finish the wizard

### 5. Configure the WSGI File

1. On the **Web** tab, scroll down to the **Code** section
2. Click on the **WSGI configuration file** link (it will be something like `/var/www/yourusername_pythonanywhere_com_wsgi.py`)
3. Delete all the existing content
4. Replace it with the content from the `wsgi.py` file in this repository, but **make sure to update the paths**:

   ```python
   import sys
   import os

   # IMPORTANT: Replace 'yourusername' with your actual PythonAnywhere username
   # Or set PROJECT_HOME environment variable to avoid editing this file
   project_home = os.environ.get('PROJECT_HOME', '/home/yourusername/HobbyBudgetTracker')
   if project_home not in sys.path:
       sys.path = [project_home] + sys.path

   # Set the database path to a writable location
   # You can set DB_PATH environment variable to override
   db_path = os.environ.get('DB_PATH', os.path.join(project_home, 'hobby_budget.db'))

   # Import the Flask app
   from hobby_budget_tracker.web import create_app

   # Create the application instance
   application = create_app(db_path=db_path)
   ```

5. **Critical**: Either:
   - Replace `yourusername` with your actual PythonAnywhere username in the default path, OR
   - Set the `PROJECT_HOME` environment variable (see Environment Variables section below)
6. Click **Save**

#### Setting Environment Variables (Optional)

Instead of editing the WSGI file, you can set environment variables on PythonAnywhere:

1. On the **Web** tab, scroll to the **Environment variables** section
2. Click **Add a new environment variable**
3. Set:
   - **Name**: `PROJECT_HOME`
   - **Value**: `/home/yourusername/HobbyBudgetTracker` (with your actual username)
4. Optionally, set `DB_PATH` if you want to use a different database location

### 6. Set Up the Virtual Environment in Web App Configuration

1. Still on the **Web** tab, scroll to the **Virtualenv** section
2. Click **Enter path to a virtualenv, if desired**
3. Enter the path to your virtual environment:
   ```
   /home/yourusername/.virtualenvs/hobby-budget-env
   ```
   Replace `yourusername` with your actual PythonAnywhere username
4. The path should turn green if it's correct

### 7. Set Up Static Files (if needed)

The Hobby Budget Tracker embeds all CSS and JavaScript in the HTML template, so no separate static files configuration is needed. However, if you add static files later:

1. On the **Web** tab, scroll to the **Static files** section
2. Add a new entry:
   - **URL**: `/static/`
   - **Directory**: `/home/yourusername/HobbyBudgetTracker/hobby_budget_tracker/static`

### 8. Initialize the Database

1. Go back to your **Bash console** (or open a new one)
2. Activate your virtual environment if not already active:
   ```bash
   workon hobby-budget-env
   ```
3. Navigate to your project directory:
   ```bash
   cd ~/HobbyBudgetTracker
   ```
4. Create the database by running a simple Python command:
   ```bash
   python3 -c "from hobby_budget_tracker.database import Database; db = Database('hobby_budget.db'); db.close()"
   ```
   This will create the `hobby_budget.db` file with all necessary tables.

### 9. Reload Your Web App

1. Go back to the **Web** tab
2. Click the big green **Reload** button at the top
3. Wait for the reload to complete (it may take a few seconds)

### 10. Access Your Application

1. Your app will be available at: `https://yourusername.pythonanywhere.com`
2. Replace `yourusername` with your actual PythonAnywhere username
3. Open this URL in your browser to access your Hobby Budget Tracker!

## Troubleshooting

### Common Issues and Solutions

#### 1. ImportError or ModuleNotFoundError

**Problem**: You see errors like `ModuleNotFoundError: No module named 'flask'` or `No module named 'hobby_budget_tracker'`

**Solutions**:
- Make sure you've installed the package in your virtual environment: `pip install -e .`
- Verify the virtualenv path is correct in the Web tab
- Check that the project path in the WSGI file is correct

#### 2. "Something went wrong" Error Page

**Problem**: The app shows an error page instead of loading

**Solutions**:
- Check the **Error log** and **Server log** on the Web tab
- Common issues:
  - Incorrect paths in WSGI file
  - Virtual environment not properly set up
  - Missing dependencies

#### 3. Database Errors

**Problem**: Errors about database connection or locked database

**Solutions**:
- Ensure the database file path is writable
- Make sure you've initialized the database (step 8)
- The database file should be in `/home/yourusername/HobbyBudgetTracker/`

#### 4. 404 Errors on All Pages

**Problem**: All pages return 404 Not Found

**Solutions**:
- Check that `application` is the name of the Flask app in your WSGI file
- Verify the WSGI file is correctly configured
- Check the server logs for detailed error messages

### Viewing Logs

To debug issues, check the logs on the **Web** tab:

1. **Error log**: Shows Python errors and exceptions
2. **Server log**: Shows HTTP requests and responses
3. **Access log**: Shows all incoming requests

You can also tail the logs in real-time from a Bash console:
```bash
tail -f /var/log/yourusername.pythonanywhere.com.error.log
```

## Updating Your Application

### Manual Updates

When you make changes to your code:

1. Pull the latest changes in your Bash console:
   ```bash
   cd ~/HobbyBudgetTracker
   git pull origin main
   ```

2. If you added new dependencies:
   ```bash
   workon hobby-budget-env
   pip install -e .
   ```

3. Reload your web app from the **Web** tab

### Automatic Updates (Continuous Deployment)

For automated deployments when you push code to GitHub, see [CONTINUOUS_DEPLOYMENT.md](CONTINUOUS_DEPLOYMENT.md). This will:
- Automatically deploy changes when you push to the main branch
- Reload your web application
- Provide deployment status in GitHub Actions

Setting up continuous deployment is recommended for easier maintenance and faster updates.

## Database Backup

To backup your database:

```bash
cd ~/HobbyBudgetTracker
cp hobby_budget.db hobby_budget.db.backup-$(date +%Y%m%d)
```

To download a backup to your local computer:
1. Use the **Files** tab in PythonAnywhere
2. Navigate to `/home/yourusername/HobbyBudgetTracker/`
3. Click the download icon next to `hobby_budget.db`

## Performance Considerations

### Free Tier Limitations

The PythonAnywhere free tier has some limitations:
- Your app will "sleep" after being inactive
- Limited CPU seconds per day
- No HTTPS for custom domains (available on paid plans)

For a personal hobby tracker, these limitations are usually fine.

### Paid Plans

If you need better performance or custom domains:
- **Hacker Plan** ($5/month): More CPU, always-on apps, custom domains
- Higher tiers available for more resources

## Security Recommendations

1. **Change Default Settings**: For production use, consider adding:
   - A secret key for Flask sessions
   - User authentication
   - HTTPS (available on paid plans with custom domains)

2. **Regular Backups**: Backup your database regularly (see Database Backup section)

3. **Keep Dependencies Updated**:
   ```bash
   workon hobby-budget-env
   pip install --upgrade Flask
   ```

4. **Monitor Logs**: Regularly check your error logs for any issues

## Additional Resources

- [PythonAnywhere Help Pages](https://help.pythonanywhere.com/)
- [PythonAnywhere Forums](https://www.pythonanywhere.com/forums/)
- [Flask Documentation](https://flask.palletsprojects.com/)

## Support

If you encounter issues:
1. Check this troubleshooting guide
2. Review the PythonAnywhere help pages
3. Check the repository issues: https://github.com/bohlke01/HobbyBudgetTracker/issues
4. For PythonAnywhere-specific issues, contact their support through the forums

## Example: Complete Setup Commands

Here's a complete list of commands for quick reference:

```bash
# 1. Clone the repository
git clone https://github.com/bohlke01/HobbyBudgetTracker.git
cd HobbyBudgetTracker

# 2. Create and activate virtual environment
mkvirtualenv --python=/usr/bin/python3.10 hobby-budget-env

# 3. Install dependencies
pip install -e .

# 4. Initialize the database
python3 -c "from hobby_budget_tracker.database import Database; db = Database('hobby_budget.db'); db.close()"

# 5. Test the installation (optional)
python -m unittest discover tests
```

Then configure the web app as described in steps 4-6, and reload.

That's it! Your Hobby Budget Tracker should now be running on PythonAnywhere.
