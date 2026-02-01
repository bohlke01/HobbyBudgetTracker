# PythonAnywhere Quick Start Guide

## Quick Reference Commands

After logging into PythonAnywhere and opening a Bash console:

```bash
# Clone repository
git clone https://github.com/bohlke01/HobbyBudgetTracker.git
cd HobbyBudgetTracker

# Set up virtual environment
mkvirtualenv --python=/usr/bin/python3.10 hobby-budget-env

# Install application
pip install -e .

# Initialize database
python3 -c "from hobby_budget_tracker.database import Database; db = Database('hobby_budget.db'); db.close()"
```

## WSGI Configuration Template

In your PythonAnywhere Web tab, set the WSGI configuration file to:

```python
import sys
import os

# Replace 'yourusername' with your PythonAnywhere username
project_home = '/home/yourusername/HobbyBudgetTracker'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Set the database path
db_path = os.path.join(project_home, 'hobby_budget.db')

# Import and create the Flask app
from hobby_budget_tracker.web import create_app
application = create_app(db_path=db_path)
```

## Virtual Environment Path

Set in Web tab → Virtualenv section:
```
/home/yourusername/.virtualenvs/hobby-budget-env
```

## Your App URL

After setup, access your app at:
```
https://yourusername.pythonanywhere.com
```

Replace `yourusername` with your actual PythonAnywhere username.

---

For detailed instructions, see [DEPLOYMENT.md](DEPLOYMENT.md)
