"""
Tests for database operations.
"""
import unittest
import tempfile
import os
from datetime import datetime

from hobby_budget_tracker.database import Database
from hobby_budget_tracker.models import Hobby, Expense, Activity


class TestDatabase(unittest.TestCase):
    """Test database operations."""
    
    def setUp(self):
        """Set up test database."""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db = Database(self.temp_db.name)
    
    def tearDown(self):
        """Clean up test database."""
        self.db.close()
        os.unlink(self.temp_db.name)
    
    def test_add_and_get_hobby(self):
        """Test adding and retrieving a hobby."""
        hobby = Hobby(id=None, name="Photography", description="Taking photos")
        hobby_id = self.db.add_hobby(hobby)
        
        retrieved = self.db.get_hobby(hobby_id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.name, "Photography")
        self.assertEqual(retrieved.description, "Taking photos")
    
    def test_list_hobbies(self):
        """Test listing hobbies."""
        hobby1 = Hobby(id=None, name="Painting")
        hobby2 = Hobby(id=None, name="Gaming")
        
        self.db.add_hobby(hobby1)
        self.db.add_hobby(hobby2)
        
        hobbies = self.db.list_hobbies()
        self.assertEqual(len(hobbies), 2)
        names = [h.name for h in hobbies]
        self.assertIn("Painting", names)
        self.assertIn("Gaming", names)
    
    def test_get_hobby_by_name(self):
        """Test getting hobby by name."""
        hobby = Hobby(id=None, name="Cooking")
        self.db.add_hobby(hobby)
        
        retrieved = self.db.get_hobby_by_name("Cooking")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.name, "Cooking")
    
    def test_delete_hobby(self):
        """Test deleting a hobby."""
        hobby = Hobby(id=None, name="Reading")
        hobby_id = self.db.add_hobby(hobby)
        
        self.db.delete_hobby(hobby_id)
        
        retrieved = self.db.get_hobby(hobby_id)
        self.assertIsNone(retrieved)
    
    def test_add_and_list_expenses(self):
        """Test adding and listing expenses."""
        hobby = Hobby(id=None, name="Gardening")
        hobby_id = self.db.add_hobby(hobby)
        
        expense1 = Expense(id=None, hobby_id=hobby_id, amount=50.0, description="Seeds")
        expense2 = Expense(id=None, hobby_id=hobby_id, amount=30.0, description="Tools")
        
        self.db.add_expense(expense1)
        self.db.add_expense(expense2)
        
        expenses = self.db.list_expenses(hobby_id)
        self.assertEqual(len(expenses), 2)
    
    def test_get_total_expenses(self):
        """Test calculating total expenses."""
        hobby = Hobby(id=None, name="Woodworking")
        hobby_id = self.db.add_hobby(hobby)
        
        self.db.add_expense(Expense(id=None, hobby_id=hobby_id, amount=100.0))
        self.db.add_expense(Expense(id=None, hobby_id=hobby_id, amount=150.0))
        
        total = self.db.get_total_expenses(hobby_id)
        self.assertEqual(total, 250.0)
    
    def test_add_and_list_activities(self):
        """Test adding and listing activities."""
        hobby = Hobby(id=None, name="Music")
        hobby_id = self.db.add_hobby(hobby)
        
        activity1 = Activity(id=None, hobby_id=hobby_id, duration_hours=2.5)
        activity2 = Activity(id=None, hobby_id=hobby_id, duration_hours=1.0)
        
        self.db.add_activity(activity1)
        self.db.add_activity(activity2)
        
        activities = self.db.list_activities(hobby_id)
        self.assertEqual(len(activities), 2)
    
    def test_get_total_hours(self):
        """Test calculating total hours."""
        hobby = Hobby(id=None, name="Drawing")
        hobby_id = self.db.add_hobby(hobby)
        
        self.db.add_activity(Activity(id=None, hobby_id=hobby_id, duration_hours=3.0))
        self.db.add_activity(Activity(id=None, hobby_id=hobby_id, duration_hours=2.5))
        
        total = self.db.get_total_hours(hobby_id)
        self.assertEqual(total, 5.5)
    
    def test_get_expense_per_hour(self):
        """Test calculating expense per hour (KPI)."""
        hobby = Hobby(id=None, name="Cycling")
        hobby_id = self.db.add_hobby(hobby)
        
        # Add expenses
        self.db.add_expense(Expense(id=None, hobby_id=hobby_id, amount=200.0))
        self.db.add_expense(Expense(id=None, hobby_id=hobby_id, amount=100.0))
        
        # Add activities
        self.db.add_activity(Activity(id=None, hobby_id=hobby_id, duration_hours=10.0))
        self.db.add_activity(Activity(id=None, hobby_id=hobby_id, duration_hours=5.0))
        
        # Total: 300 / 15 = 20.0
        expense_per_hour = self.db.get_expense_per_hour(hobby_id)
        self.assertIsNotNone(expense_per_hour)
        self.assertEqual(expense_per_hour, 20.0)
    
    def test_get_expense_per_hour_no_activities(self):
        """Test expense per hour returns None when no activities."""
        hobby = Hobby(id=None, name="Fishing")
        hobby_id = self.db.add_hobby(hobby)
        
        self.db.add_expense(Expense(id=None, hobby_id=hobby_id, amount=100.0))
        
        expense_per_hour = self.db.get_expense_per_hour(hobby_id)
        self.assertIsNone(expense_per_hour)
    
    def test_duplicate_hobby_name(self):
        """Test that adding a hobby with duplicate name raises error."""
        from hobby_budget_tracker.database import DuplicateHobbyError
        
        hobby1 = Hobby(id=None, name="Archery")
        self.db.add_hobby(hobby1)
        
        hobby2 = Hobby(id=None, name="Archery", description="Different description")
        with self.assertRaises(DuplicateHobbyError):
            self.db.add_hobby(hobby2)
    
    def test_add_hobby_with_target_value(self):
        """Test adding a hobby with a target value."""
        hobby = Hobby(id=None, name="Swimming", description="Water sports", target_value=15.0)
        hobby_id = self.db.add_hobby(hobby)
        
        retrieved = self.db.get_hobby(hobby_id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.name, "Swimming")
        self.assertEqual(retrieved.target_value, 15.0)
    
    def test_update_hobby_name(self):
        """Test updating a hobby's name."""
        hobby = Hobby(id=None, name="Basketball")
        hobby_id = self.db.add_hobby(hobby)
        
        self.db.update_hobby(hobby_id, name="Football")
        
        retrieved = self.db.get_hobby(hobby_id)
        self.assertEqual(retrieved.name, "Football")
    
    def test_update_hobby_description(self):
        """Test updating a hobby's description."""
        hobby = Hobby(id=None, name="Skiing", description="Winter sport")
        hobby_id = self.db.add_hobby(hobby)
        
        self.db.update_hobby(hobby_id, description="Snow sport")
        
        retrieved = self.db.get_hobby(hobby_id)
        self.assertEqual(retrieved.description, "Snow sport")
    
    def test_update_hobby_target_value(self):
        """Test updating a hobby's target value."""
        hobby = Hobby(id=None, name="Tennis", target_value=10.0)
        hobby_id = self.db.add_hobby(hobby)
        
        self.db.update_hobby(hobby_id, target_value=20.0)
        
        retrieved = self.db.get_hobby(hobby_id)
        self.assertEqual(retrieved.target_value, 20.0)
    
    def test_update_hobby_duplicate_name(self):
        """Test that updating a hobby to a duplicate name raises error."""
        from hobby_budget_tracker.database import DuplicateHobbyError
        
        hobby1 = Hobby(id=None, name="Volleyball")
        hobby2 = Hobby(id=None, name="Baseball")
        hobby1_id = self.db.add_hobby(hobby1)
        self.db.add_hobby(hobby2)
        
        with self.assertRaises(DuplicateHobbyError):
            self.db.update_hobby(hobby1_id, name="Baseball")
    
    def test_get_expense_per_hour_time_series(self):
        """Test getting expense per hour time series."""
        hobby = Hobby(id=None, name="Photography")
        hobby_id = self.db.add_hobby(hobby)
        
        # Add expenses on different dates
        expense1 = Expense(id=None, hobby_id=hobby_id, amount=100.0, date=datetime(2024, 1, 1))
        expense2 = Expense(id=None, hobby_id=hobby_id, amount=50.0, date=datetime(2024, 1, 5))
        self.db.add_expense(expense1)
        self.db.add_expense(expense2)
        
        # Add activities on different dates
        activity1 = Activity(id=None, hobby_id=hobby_id, duration_hours=5.0, date=datetime(2024, 1, 1))
        activity2 = Activity(id=None, hobby_id=hobby_id, duration_hours=5.0, date=datetime(2024, 1, 5))
        self.db.add_activity(activity1)
        self.db.add_activity(activity2)
        
        time_series = self.db.get_expense_per_hour_time_series(hobby_id)
        
        # Should have 2 data points
        self.assertEqual(len(time_series), 2)
        
        # First point: 100 / 5 = 20.0
        self.assertEqual(time_series[0]['date'], '2024-01-01')
        self.assertEqual(time_series[0]['expense_per_hour'], 20.0)
        
        # Second point: (100 + 50) / (5 + 5) = 15.0 (cumulative)
        self.assertEqual(time_series[1]['date'], '2024-01-05')
        self.assertEqual(time_series[1]['expense_per_hour'], 15.0)
    
    def test_get_expense_per_hour_time_series_no_activities(self):
        """Test time series returns empty list when no activities."""
        hobby = Hobby(id=None, name="Painting")
        hobby_id = self.db.add_hobby(hobby)
        
        # Add only expense, no activities
        expense = Expense(id=None, hobby_id=hobby_id, amount=100.0, date=datetime(2024, 1, 1))
        self.db.add_expense(expense)
        
        time_series = self.db.get_expense_per_hour_time_series(hobby_id)
        
        # Should have no data points since no activities (division by zero)
        self.assertEqual(len(time_series), 0)
    
    def test_get_expense_per_hour_time_series_ordering(self):
        """Test time series is ordered by date."""
        hobby = Hobby(id=None, name="Gaming")
        hobby_id = self.db.add_hobby(hobby)
        
        # Add data in non-chronological order
        expense1 = Expense(id=None, hobby_id=hobby_id, amount=50.0, date=datetime(2024, 1, 10))
        expense2 = Expense(id=None, hobby_id=hobby_id, amount=100.0, date=datetime(2024, 1, 5))
        self.db.add_expense(expense1)
        self.db.add_expense(expense2)
        
        activity1 = Activity(id=None, hobby_id=hobby_id, duration_hours=2.0, date=datetime(2024, 1, 10))
        activity2 = Activity(id=None, hobby_id=hobby_id, duration_hours=5.0, date=datetime(2024, 1, 5))
        self.db.add_activity(activity1)
        self.db.add_activity(activity2)
        
        time_series = self.db.get_expense_per_hour_time_series(hobby_id)
        
        # Should be ordered by date
        self.assertEqual(len(time_series), 2)
        self.assertEqual(time_series[0]['date'], '2024-01-05')
        self.assertEqual(time_series[1]['date'], '2024-01-10')


if __name__ == '__main__':
    unittest.main()
