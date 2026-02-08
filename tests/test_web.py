"""
Tests for web interface.
"""
import unittest
import tempfile
import os
import json

from hobby_budget_tracker.web import create_app
from hobby_budget_tracker.models import Hobby, Expense, Activity


class TestWebInterface(unittest.TestCase):
    """Test web interface operations."""
    
    def setUp(self):
        """Set up test client."""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.app = create_app(self.temp_db.name)
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def tearDown(self):
        """Clean up test database."""
        os.unlink(self.temp_db.name)
    
    def test_index_route(self):
        """Test that index route returns 200."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_add_hobby_api(self):
        """Test adding a hobby via API."""
        response = self.client.post('/api/hobbies',
                                   json={'name': 'Hiking', 'description': 'Outdoor activity'})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['message'], 'Hobby added successfully')
    
    def test_add_hobby_with_target_value(self):
        """Test adding a hobby with target value via API."""
        response = self.client.post('/api/hobbies',
                                   json={'name': 'Running', 'target_value': 15.5})
        self.assertEqual(response.status_code, 201)
        
        # Retrieve and verify
        response = self.client.get('/api/hobbies')
        hobbies = json.loads(response.data)
        self.assertEqual(len(hobbies), 1)
        self.assertEqual(hobbies[0]['name'], 'Running')
        self.assertEqual(hobbies[0]['target_value'], 15.5)
    
    def test_get_hobbies_api(self):
        """Test getting hobbies via API."""
        # Add a hobby first
        self.client.post('/api/hobbies', json={'name': 'Reading'})
        
        response = self.client.get('/api/hobbies')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'Reading')
    
    def test_delete_hobby_api(self):
        """Test deleting a hobby via API."""
        # Add a hobby first
        response = self.client.post('/api/hobbies', json={'name': 'Cooking'})
        hobby_id = json.loads(response.data)['id']
        
        # Delete it
        response = self.client.delete(f'/api/hobbies/{hobby_id}')
        self.assertEqual(response.status_code, 200)
        
        # Verify it's gone
        response = self.client.get('/api/hobbies')
        data = json.loads(response.data)
        self.assertEqual(len(data), 0)
    
    def test_update_hobby_api(self):
        """Test updating a hobby via API."""
        # Add a hobby first
        response = self.client.post('/api/hobbies', json={'name': 'Gardening'})
        hobby_id = json.loads(response.data)['id']
        
        # Update it
        response = self.client.put(f'/api/hobbies/{hobby_id}',
                                   json={'name': 'Gardening', 'description': 'Growing plants', 'target_value': 12.0})
        self.assertEqual(response.status_code, 200)
        
        # Verify update
        response = self.client.get('/api/hobbies')
        hobbies = json.loads(response.data)
        self.assertEqual(hobbies[0]['description'], 'Growing plants')
        self.assertEqual(hobbies[0]['target_value'], 12.0)
    
    def test_add_expense_api(self):
        """Test adding an expense via API."""
        # Add a hobby first
        response = self.client.post('/api/hobbies', json={'name': 'Fishing'})
        hobby_id = json.loads(response.data)['id']
        
        # Add expense with date
        response = self.client.post('/api/expenses',
                                   json={'hobby_id': hobby_id, 'amount': 99.99, 'description': 'Fishing rod', 'date': '2024-01-01T10:00:00'})
        self.assertEqual(response.status_code, 201)
    
    def test_get_expenses_api(self):
        """Test getting expenses via API."""
        # Add a hobby and expense
        response = self.client.post('/api/hobbies', json={'name': 'Painting'})
        hobby_id = json.loads(response.data)['id']
        self.client.post('/api/expenses',
                        json={'hobby_id': hobby_id, 'amount': 50.0, 'date': '2024-01-01T10:00:00'})
        
        response = self.client.get(f'/api/expenses?hobby_id={hobby_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['amount'], 50.0)
    
    def test_add_activity_api(self):
        """Test adding an activity via API."""
        # Add a hobby first
        response = self.client.post('/api/hobbies', json={'name': 'Swimming'})
        hobby_id = json.loads(response.data)['id']
        
        # Add activity with date
        response = self.client.post('/api/activities',
                                   json={'hobby_id': hobby_id, 'duration_hours': 2.5, 'date': '2024-01-01T10:00:00'})
        self.assertEqual(response.status_code, 201)
    
    def test_get_activities_api(self):
        """Test getting activities via API."""
        # Add a hobby and activity
        response = self.client.post('/api/hobbies', json={'name': 'Cycling'})
        hobby_id = json.loads(response.data)['id']
        self.client.post('/api/activities',
                        json={'hobby_id': hobby_id, 'duration_hours': 3.0, 'date': '2024-01-01T10:00:00'})
        
        response = self.client.get(f'/api/activities?hobby_id={hobby_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['duration_hours'], 3.0)
    
    def test_get_hobby_stats_api(self):
        """Test getting hobby statistics via API."""
        # Add a hobby with expenses and activities
        response = self.client.post('/api/hobbies', json={'name': 'Music'})
        hobby_id = json.loads(response.data)['id']
        self.client.post('/api/expenses', json={'hobby_id': hobby_id, 'amount': 200.0, 'date': '2024-01-01T10:00:00'})
        self.client.post('/api/activities', json={'hobby_id': hobby_id, 'duration_hours': 10.0, 'date': '2024-01-01T10:00:00'})
        
        response = self.client.get(f'/api/hobbies/{hobby_id}/stats')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['total_expenses'], 200.0)
        self.assertEqual(data['total_hours'], 10.0)
        self.assertEqual(data['expense_per_hour'], 20.0)
    
    def test_get_hobby_chart_data_api(self):
        """Test getting hobby chart data via API."""
        # Add a hobby with target value
        response = self.client.post('/api/hobbies', json={'name': 'Photography', 'target_value': 25.0})
        hobby_id = json.loads(response.data)['id']
        
        # Add some expenses and activities
        self.client.post('/api/expenses', json={'hobby_id': hobby_id, 'amount': 100.0, 'date': '2024-01-01T00:00:00'})
        self.client.post('/api/activities', json={'hobby_id': hobby_id, 'duration_hours': 5.0, 'date': '2024-01-01T00:00:00'})
        
        response = self.client.get(f'/api/hobbies/{hobby_id}/chart-data')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('time_series', data)
        self.assertEqual(data['target_value'], 25.0)
        self.assertEqual(len(data['time_series']), 1)
    
    def test_get_summary_api(self):
        """Test getting summary via API."""
        # Add multiple hobbies with data
        response = self.client.post('/api/hobbies', json={'name': 'Gaming'})
        hobby_id1 = json.loads(response.data)['id']
        self.client.post('/api/expenses', json={'hobby_id': hobby_id1, 'amount': 100.0, 'date': '2024-01-01T10:00:00'})
        self.client.post('/api/activities', json={'hobby_id': hobby_id1, 'duration_hours': 5.0, 'date': '2024-01-01T10:00:00'})
        
        response = self.client.post('/api/hobbies', json={'name': 'Drawing'})
        hobby_id2 = json.loads(response.data)['id']
        self.client.post('/api/expenses', json={'hobby_id': hobby_id2, 'amount': 50.0, 'date': '2024-01-01T10:00:00'})
        self.client.post('/api/activities', json={'hobby_id': hobby_id2, 'duration_hours': 2.0, 'date': '2024-01-01T10:00:00'})
        
        response = self.client.get('/api/summary')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['expense_per_hour'], 25.0)  # Drawing: 50/2=25 (sorted by name)
        self.assertEqual(data[1]['expense_per_hour'], 20.0)  # Gaming: 100/5=20
    
    def test_duplicate_hobby_error(self):
        """Test that adding duplicate hobby returns error."""
        self.client.post('/api/hobbies', json={'name': 'Tennis'})
        response = self.client.post('/api/hobbies', json={'name': 'Tennis'})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_update_nonexistent_hobby(self):
        """Test updating a hobby that doesn't exist."""
        response = self.client.put('/api/hobbies/999',
                                   json={'name': 'Test'})
        self.assertEqual(response.status_code, 404)
    
    def test_delete_nonexistent_hobby(self):
        """Test deleting a hobby that doesn't exist."""
        response = self.client.delete('/api/hobbies/999')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
