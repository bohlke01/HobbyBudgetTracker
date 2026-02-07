"""
Database management for Hobby Budget Tracker using SQLite.
"""
import sqlite3
from pathlib import Path
from typing import List, Optional
from datetime import datetime

from .models import Hobby, Expense, Activity


class DuplicateHobbyError(Exception):
    """Raised when attempting to add a hobby with a duplicate name."""
    pass


class Database:
    """Manages SQLite database operations."""
    
    def __init__(self, db_path: str = "hobby_budget.db"):
        """Initialize database connection."""
        self.db_path = db_path
        self.conn = None
        self._connect()
        self._create_tables()
    
    def _connect(self):
        """Establish database connection."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
    
    @staticmethod
    def _row_to_hobby(row) -> Hobby:
        """Convert database row to Hobby object."""
        return Hobby(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            created_at=datetime.fromisoformat(row["created_at"])
        )
    
    @staticmethod
    def _row_to_expense(row) -> Expense:
        """Convert database row to Expense object."""
        return Expense(
            id=row["id"],
            hobby_id=row["hobby_id"],
            amount=row["amount"],
            description=row["description"],
            date=datetime.fromisoformat(row["date"])
        )
    
    @staticmethod
    def _row_to_activity(row) -> Activity:
        """Convert database row to Activity object."""
        return Activity(
            id=row["id"],
            hobby_id=row["hobby_id"],
            duration_hours=row["duration_hours"],
            description=row["description"],
            date=datetime.fromisoformat(row["date"])
        )
    
    def _create_tables(self):
        """Create database tables if they don't exist."""
        cursor = self.conn.cursor()
        
        # Hobbies table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hobbies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                created_at TEXT NOT NULL
            )
        """)
        
        # Expenses table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hobby_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                date TEXT NOT NULL,
                FOREIGN KEY (hobby_id) REFERENCES hobbies (id)
            )
        """)
        
        # Activities table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hobby_id INTEGER NOT NULL,
                duration_hours REAL NOT NULL,
                description TEXT,
                date TEXT NOT NULL,
                FOREIGN KEY (hobby_id) REFERENCES hobbies (id)
            )
        """)
        
        self.conn.commit()
    
    # Hobby operations
    def add_hobby(self, hobby: Hobby) -> int:
        """Add a new hobby to the database."""
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO hobbies (name, description, created_at) VALUES (?, ?, ?)",
                (hobby.name, hobby.description, hobby.created_at.isoformat())
            )
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            raise DuplicateHobbyError(f"A hobby with the name '{hobby.name}' already exists")
    
    def get_hobby(self, hobby_id: int) -> Optional[Hobby]:
        """Get a hobby by ID."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM hobbies WHERE id = ?", (hobby_id,))
        row = cursor.fetchone()
        return self._row_to_hobby(row) if row else None
    
    def get_hobby_by_name(self, name: str) -> Optional[Hobby]:
        """Get a hobby by name."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM hobbies WHERE name = ?", (name,))
        row = cursor.fetchone()
        return self._row_to_hobby(row) if row else None
    
    def list_hobbies(self) -> List[Hobby]:
        """List all hobbies."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM hobbies ORDER BY name")
        return [self._row_to_hobby(row) for row in cursor.fetchall()]
    
    def delete_hobby(self, hobby_id: int):
        """Delete a hobby and all related expenses and activities."""
        cursor = self.conn.cursor()
        try:
            cursor.execute("DELETE FROM activities WHERE hobby_id = ?", (hobby_id,))
            cursor.execute("DELETE FROM expenses WHERE hobby_id = ?", (hobby_id,))
            cursor.execute("DELETE FROM hobbies WHERE id = ?", (hobby_id,))
            self.conn.commit()
        except sqlite3.Error:
            self.conn.rollback()
            raise
    
    # Expense operations
    def add_expense(self, expense: Expense) -> int:
        """Add a new expense to the database."""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO expenses (hobby_id, amount, description, date) VALUES (?, ?, ?, ?)",
            (expense.hobby_id, expense.amount, expense.description, expense.date.isoformat())
        )
        self.conn.commit()
        return cursor.lastrowid
    
    def list_expenses(self, hobby_id: Optional[int] = None) -> List[Expense]:
        """List expenses, optionally filtered by hobby."""
        cursor = self.conn.cursor()
        if hobby_id is not None:
            cursor.execute("SELECT * FROM expenses WHERE hobby_id = ? ORDER BY date DESC", (hobby_id,))
        else:
            cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
        return [self._row_to_expense(row) for row in cursor.fetchall()]
    
    def get_total_expenses(self, hobby_id: int) -> float:
        """Get total expenses for a hobby."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT SUM(amount) as total FROM expenses WHERE hobby_id = ?", (hobby_id,))
        row = cursor.fetchone()
        return row["total"] if row["total"] is not None else 0.0
    
    # Activity operations
    def add_activity(self, activity: Activity) -> int:
        """Add a new activity to the database."""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO activities (hobby_id, duration_hours, description, date) VALUES (?, ?, ?, ?)",
            (activity.hobby_id, activity.duration_hours, activity.description, activity.date.isoformat())
        )
        self.conn.commit()
        return cursor.lastrowid
    
    def list_activities(self, hobby_id: Optional[int] = None) -> List[Activity]:
        """List activities, optionally filtered by hobby."""
        cursor = self.conn.cursor()
        if hobby_id is not None:
            cursor.execute("SELECT * FROM activities WHERE hobby_id = ? ORDER BY date DESC", (hobby_id,))
        else:
            cursor.execute("SELECT * FROM activities ORDER BY date DESC")
        return [self._row_to_activity(row) for row in cursor.fetchall()]
    
    def get_total_hours(self, hobby_id: int) -> float:
        """Get total hours spent on a hobby."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT SUM(duration_hours) as total FROM activities WHERE hobby_id = ?", (hobby_id,))
        row = cursor.fetchone()
        return row["total"] if row["total"] is not None else 0.0
    
    # KPI calculation
    def get_expense_per_hour(self, hobby_id: int) -> Optional[float]:
        """Calculate expense per hour for a hobby."""
        total_expenses = self.get_total_expenses(hobby_id)
        total_hours = self.get_total_hours(hobby_id)
        
        if total_hours > 0:
            return total_expenses / total_hours
        return None
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
