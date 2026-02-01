"""
WSGI configuration for Hobby Budget Tracker on PythonAnywhere.

This file is used by PythonAnywhere to run the Flask application.
"""
import sys
import os

# Add your project directory to the sys.path
# You can set the PROJECT_HOME environment variable, or edit the default path below
project_home = os.environ.get('PROJECT_HOME', '/home/yourusername/HobbyBudgetTracker')
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Set the database path to a writable location
# PythonAnywhere requires the database to be in your home directory
# You can set DB_PATH environment variable to override
db_path = os.environ.get('DB_PATH', os.path.join(project_home, 'hobby_budget.db'))

# Import the Flask app
from hobby_budget_tracker.web import create_app

# Create the application instance
application = create_app(db_path=db_path)

# For debugging purposes (remove in production)
# application.config['DEBUG'] = False
