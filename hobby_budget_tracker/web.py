"""
Web interface for Hobby Budget Tracker using Flask.
"""
import os
from flask import Flask, render_template, request, jsonify, send_from_directory, g
from pathlib import Path
from datetime import datetime

from .database import Database, DuplicateHobbyError
from .models import Hobby, Expense, Activity


def create_app(db_path: str = "hobby_budget.db"):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Configure paths
    template_folder = Path(__file__).parent / "templates"
    static_folder = Path(__file__).parent / "static"
    
    app.template_folder = str(template_folder)
    app.static_folder = str(static_folder)
    app.config['DB_PATH'] = db_path
    
    def get_db():
        """Get database connection for current request."""
        if 'db' not in g:
            g.db = Database(app.config['DB_PATH'])
        return g.db
    
    @staticmethod
    def _serialize_hobby(hobby: Hobby) -> dict:
        """Convert Hobby to JSON-serializable dict."""
        return {
            'id': hobby.id,
            'name': hobby.name,
            'description': hobby.description,
            'created_at': hobby.created_at.isoformat()
        }
    
    @staticmethod
    def _serialize_expense(expense: Expense) -> dict:
        """Convert Expense to JSON-serializable dict."""
        return {
            'id': expense.id,
            'hobby_id': expense.hobby_id,
            'amount': expense.amount,
            'description': expense.description,
            'date': expense.date.isoformat()
        }
    
    @staticmethod
    def _serialize_activity(activity: Activity) -> dict:
        """Convert Activity to JSON-serializable dict."""
        return {
            'id': activity.id,
            'hobby_id': activity.hobby_id,
            'duration_hours': activity.duration_hours,
            'description': activity.description,
            'date': activity.date.isoformat()
        }
    
    @app.teardown_appcontext
    def close_db(error):
        """Close database connection at end of request."""
        db = g.pop('db', None)
        if db is not None:
            db.close()
    
    @app.route('/')
    def index():
        """Render the main page."""
        return render_template('index.html')
    
    # API Routes for Hobbies
    @app.route('/api/hobbies', methods=['GET'])
    def get_hobbies():
        """Get all hobbies."""
        db = get_db()
        hobbies = db.list_hobbies()
        return jsonify([_serialize_hobby(h) for h in hobbies])
    
    @app.route('/api/hobbies', methods=['POST'])
    def add_hobby():
        """Add a new hobby."""
        db = get_db()
        data = request.get_json()
        try:
            hobby = Hobby(
                id=None,
                name=data['name'],
                description=data.get('description', '')
            )
            hobby_id = db.add_hobby(hobby)
            return jsonify({'id': hobby_id, 'message': 'Hobby added successfully'}), 201
        except DuplicateHobbyError as e:
            return jsonify({'error': str(e)}), 400
        except KeyError:
            return jsonify({'error': 'Missing required field: name'}), 400
    
    @app.route('/api/hobbies/<int:hobby_id>', methods=['DELETE'])
    def delete_hobby(hobby_id):
        """Delete a hobby."""
        db = get_db()
        hobby = db.get_hobby(hobby_id)
        if not hobby:
            return jsonify({'error': 'Hobby not found'}), 404
        db.delete_hobby(hobby_id)
        return jsonify({'message': 'Hobby deleted successfully'}), 200
    
    @app.route('/api/hobbies/<int:hobby_id>/stats', methods=['GET'])
    def get_hobby_stats(hobby_id):
        """Get statistics for a hobby."""
        db = get_db()
        hobby = db.get_hobby(hobby_id)
        if not hobby:
            return jsonify({'error': 'Hobby not found'}), 404
        
        total_expenses = db.get_total_expenses(hobby_id)
        total_hours = db.get_total_hours(hobby_id)
        expense_per_hour = db.get_expense_per_hour(hobby_id)
        
        return jsonify({
            'hobby': {
                'id': hobby.id,
                'name': hobby.name,
                'description': hobby.description
            },
            'total_expenses': total_expenses,
            'total_hours': total_hours,
            'expense_per_hour': expense_per_hour
        })
    
    # API Routes for Expenses
    @app.route('/api/expenses', methods=['GET'])
    def get_expenses():
        """Get all expenses, optionally filtered by hobby."""
        db = get_db()
        hobby_id = request.args.get('hobby_id', type=int)
        expenses = db.list_expenses(hobby_id)
        return jsonify([_serialize_expense(e) for e in expenses])
    
    @app.route('/api/expenses', methods=['POST'])
    def add_expense():
        """Add a new expense."""
        db = get_db()
        data = request.get_json()
        try:
            expense = Expense(
                id=None,
                hobby_id=data['hobby_id'],
                amount=float(data['amount']),
                description=data.get('description', '')
            )
            expense_id = db.add_expense(expense)
            return jsonify({'id': expense_id, 'message': 'Expense added successfully'}), 201
        except KeyError as e:
            return jsonify({'error': f'Missing required field: {str(e)}'}), 400
        except ValueError:
            return jsonify({'error': 'Invalid amount value'}), 400
    
    # API Routes for Activities
    @app.route('/api/activities', methods=['GET'])
    def get_activities():
        """Get all activities, optionally filtered by hobby."""
        db = get_db()
        hobby_id = request.args.get('hobby_id', type=int)
        activities = db.list_activities(hobby_id)
        return jsonify([_serialize_activity(a) for a in activities])
    
    @app.route('/api/activities', methods=['POST'])
    def add_activity():
        """Add a new activity."""
        db = get_db()
        data = request.get_json()
        try:
            activity = Activity(
                id=None,
                hobby_id=data['hobby_id'],
                duration_hours=float(data['duration_hours']),
                description=data.get('description', '')
            )
            activity_id = db.add_activity(activity)
            return jsonify({'id': activity_id, 'message': 'Activity added successfully'}), 201
        except KeyError as e:
            return jsonify({'error': f'Missing required field: {str(e)}'}), 400
        except ValueError:
            return jsonify({'error': 'Invalid duration value'}), 400
    
    # Summary endpoint
    @app.route('/api/summary', methods=['GET'])
    def get_summary():
        """Get summary of all hobbies."""
        db = get_db()
        hobbies = db.list_hobbies()
        summary = []
        for hobby in hobbies:
            total_expenses = db.get_total_expenses(hobby.id)
            total_hours = db.get_total_hours(hobby.id)
            expense_per_hour = db.get_expense_per_hour(hobby.id)
            summary.append({
                'id': hobby.id,
                'name': hobby.name,
                'description': hobby.description,
                'total_expenses': total_expenses,
                'total_hours': total_hours,
                'expense_per_hour': expense_per_hour
            })
        return jsonify(summary)
    
    return app


def main():
    """Main entry point for web interface."""
    import os
    app = create_app()
    debug_mode = os.environ.get('FLASK_DEBUG', '0') == '1'
    print("Starting Hobby Budget Tracker Web Interface...")
    print("Access the application at: http://localhost:5000")
    if not debug_mode:
        print("Note: Running in production mode. Set FLASK_DEBUG=1 for debug mode.")
    print("Press Ctrl+C to stop the server")
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)


if __name__ == "__main__":
    main()
