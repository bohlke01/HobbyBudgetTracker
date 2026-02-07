"""
Data models for Hobby Budget Tracker.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


def default_datetime():
    """Factory function for default datetime."""
    return datetime.now()


@dataclass
class Hobby:
    """Represents a hobby being tracked."""
    id: Optional[int]
    name: str
    description: str = ""
    created_at: datetime = field(default_factory=default_datetime)
    target_value: Optional[float] = None  # Target expense per hour (e.g., 10 euros/hour)


@dataclass
class Expense:
    """Represents an expense for a hobby."""
    id: Optional[int]
    hobby_id: int
    amount: float
    description: str = ""
    date: datetime = field(default_factory=default_datetime)


@dataclass
class Activity:
    """Represents an activity session for a hobby."""
    id: Optional[int]
    hobby_id: int
    duration_hours: float
    description: str = ""
    date: datetime = field(default_factory=default_datetime)
