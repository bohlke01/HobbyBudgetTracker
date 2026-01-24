"""
Data models for Hobby Budget Tracker.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Hobby:
    """Represents a hobby being tracked."""
    id: Optional[int]
    name: str
    description: str = ""
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class Expense:
    """Represents an expense for a hobby."""
    id: Optional[int]
    hobby_id: int
    amount: float
    description: str = ""
    date: datetime = None
    
    def __post_init__(self):
        if self.date is None:
            self.date = datetime.now()


@dataclass
class Activity:
    """Represents an activity session for a hobby."""
    id: Optional[int]
    hobby_id: int
    duration_hours: float
    description: str = ""
    date: datetime = None
    
    def __post_init__(self):
        if self.date is None:
            self.date = datetime.now()
