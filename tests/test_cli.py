"""
Tests for CLI functionality.
"""
import unittest
import tempfile
import os
import sys
from io import StringIO

from hobby_budget_tracker.cli import CLI


class TestCLI(unittest.TestCase):
    """Test CLI operations."""
    
    def setUp(self):
        """Set up test CLI."""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.cli = CLI(self.temp_db.name)
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr
    
    def tearDown(self):
        """Clean up test CLI."""
        self.cli.db.close()
        os.unlink(self.temp_db.name)
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr
    
    def capture_output(self, func):
        """Capture stdout and stderr."""
        sys.stdout = StringIO()
        sys.stderr = StringIO()
        result = func()
        stdout_value = sys.stdout.getvalue()
        stderr_value = sys.stderr.getvalue()
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr
        return result, stdout_value, stderr_value
    
    def test_add_hobby(self):
        """Test adding a hobby via CLI."""
        result, stdout, stderr = self.capture_output(
            lambda: self.cli.run(['hobby', 'add', 'Photography', '--description', 'Taking photos'])
        )
        self.assertEqual(result, 0)
        self.assertIn("Added hobby 'Photography'", stdout)
    
    def test_list_hobbies(self):
        """Test listing hobbies via CLI."""
        self.cli.run(['hobby', 'add', 'Painting'])
        self.cli.run(['hobby', 'add', 'Gaming'])
        
        result, stdout, stderr = self.capture_output(
            lambda: self.cli.run(['hobby', 'list'])
        )
        self.assertEqual(result, 0)
        self.assertIn("Painting", stdout)
        self.assertIn("Gaming", stdout)
    
    def test_add_expense(self):
        """Test adding an expense via CLI."""
        self.cli.run(['hobby', 'add', 'Cooking'])
        
        result, stdout, stderr = self.capture_output(
            lambda: self.cli.run(['expense', 'add', 'Cooking', '50.00', '--description', 'Ingredients'])
        )
        self.assertEqual(result, 0)
        self.assertIn("Added expense", stdout)
    
    def test_add_activity(self):
        """Test adding an activity via CLI."""
        self.cli.run(['hobby', 'add', 'Running'])
        
        result, stdout, stderr = self.capture_output(
            lambda: self.cli.run(['activity', 'add', 'Running', '2.5', '--description', 'Morning run'])
        )
        self.assertEqual(result, 0)
        self.assertIn("Added activity", stdout)
    
    def test_hobby_stats(self):
        """Test hobby statistics via CLI."""
        self.cli.run(['hobby', 'add', 'Cycling'])
        self.cli.run(['expense', 'add', 'Cycling', '300.00'])
        self.cli.run(['activity', 'add', 'Cycling', '10.0'])
        
        result, stdout, stderr = self.capture_output(
            lambda: self.cli.run(['hobby', 'stats', 'Cycling'])
        )
        self.assertEqual(result, 0)
        self.assertIn("Total Expenses", stdout)
        self.assertIn("Total Hours", stdout)
        self.assertIn("Cost per Hour", stdout)
        self.assertIn("30.00", stdout)  # 300/10 = 30
    
    def test_summary(self):
        """Test summary command via CLI."""
        self.cli.run(['hobby', 'add', 'Drawing'])
        self.cli.run(['expense', 'add', 'Drawing', '100.00'])
        self.cli.run(['activity', 'add', 'Drawing', '5.0'])
        
        result, stdout, stderr = self.capture_output(
            lambda: self.cli.run(['summary'])
        )
        self.assertEqual(result, 0)
        self.assertIn("HOBBY BUDGET SUMMARY", stdout)
        self.assertIn("Drawing", stdout)
        self.assertIn("20.00", stdout)  # 100/5 = 20


if __name__ == '__main__':
    unittest.main()
