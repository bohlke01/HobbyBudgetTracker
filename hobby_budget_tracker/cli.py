"""
Command-line interface for Hobby Budget Tracker.
"""
import argparse
import sys
from datetime import datetime
from typing import Optional

from .database import Database, DuplicateHobbyError
from .models import Hobby, Expense, Activity


class CLI:
    """Command-line interface handler."""
    
    def __init__(self, db_path: str = "hobby_budget.db"):
        """Initialize CLI with database."""
        self.db = Database(db_path)
    
    def run(self, args=None):
        """Run the CLI with provided arguments."""
        parser = argparse.ArgumentParser(
            description="Hobby Budget Tracker - Track expenses and activities for your hobbies"
        )
        subparsers = parser.add_subparsers(dest="command", help="Available commands")
        
        # Hobby commands
        hobby_parser = subparsers.add_parser("hobby", help="Manage hobbies")
        hobby_subparsers = hobby_parser.add_subparsers(dest="hobby_command")
        
        # hobby add
        add_hobby = hobby_subparsers.add_parser("add", help="Add a new hobby")
        add_hobby.add_argument("name", help="Hobby name")
        add_hobby.add_argument("--description", "-d", default="", help="Hobby description")
        
        # hobby list
        hobby_subparsers.add_parser("list", help="List all hobbies")
        
        # hobby delete
        delete_hobby = hobby_subparsers.add_parser("delete", help="Delete a hobby")
        delete_hobby.add_argument("name", help="Hobby name")
        
        # hobby stats
        stats_hobby = hobby_subparsers.add_parser("stats", help="Show hobby statistics")
        stats_hobby.add_argument("name", help="Hobby name")
        
        # Expense commands
        expense_parser = subparsers.add_parser("expense", help="Manage expenses")
        expense_subparsers = expense_parser.add_subparsers(dest="expense_command")
        
        # expense add
        add_expense = expense_subparsers.add_parser("add", help="Add an expense")
        add_expense.add_argument("hobby", help="Hobby name")
        add_expense.add_argument("amount", type=float, help="Expense amount")
        add_expense.add_argument("--description", "-d", default="", help="Expense description")
        
        # expense list
        list_expense = expense_subparsers.add_parser("list", help="List expenses")
        list_expense.add_argument("--hobby", help="Filter by hobby name")
        
        # Activity commands
        activity_parser = subparsers.add_parser("activity", help="Manage activities")
        activity_subparsers = activity_parser.add_subparsers(dest="activity_command")
        
        # activity add
        add_activity = activity_subparsers.add_parser("add", help="Add an activity")
        add_activity.add_argument("hobby", help="Hobby name")
        add_activity.add_argument("hours", type=float, help="Duration in hours")
        add_activity.add_argument("--description", "-d", default="", help="Activity description")
        
        # activity list
        list_activity = activity_subparsers.add_parser("list", help="List activities")
        list_activity.add_argument("--hobby", help="Filter by hobby name")
        
        # Summary command
        subparsers.add_parser("summary", help="Show summary of all hobbies")
        
        parsed_args = parser.parse_args(args)
        
        if not parsed_args.command:
            parser.print_help()
            return 1
        
        try:
            if parsed_args.command == "hobby":
                return self._handle_hobby_command(parsed_args)
            elif parsed_args.command == "expense":
                return self._handle_expense_command(parsed_args)
            elif parsed_args.command == "activity":
                return self._handle_activity_command(parsed_args)
            elif parsed_args.command == "summary":
                return self._handle_summary_command()
            else:
                parser.print_help()
                return 1
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
    
    def _handle_hobby_command(self, args):
        """Handle hobby subcommands."""
        if args.hobby_command == "add":
            hobby = Hobby(id=None, name=args.name, description=args.description)
            try:
                hobby_id = self.db.add_hobby(hobby)
                print(f"✓ Added hobby '{args.name}' (ID: {hobby_id})")
                return 0
            except DuplicateHobbyError as e:
                print(f"Error: {e}", file=sys.stderr)
                return 1
        
        elif args.hobby_command == "list":
            hobbies = self.db.list_hobbies()
            if not hobbies:
                print("No hobbies found. Add one with 'hobby add <name>'")
                return 0
            
            print("\nYour Hobbies:")
            print("-" * 60)
            for hobby in hobbies:
                print(f"• {hobby.name}")
                if hobby.description:
                    print(f"  {hobby.description}")
            print()
            return 0
        
        elif args.hobby_command == "delete":
            hobby = self.db.get_hobby_by_name(args.name)
            if not hobby:
                print(f"Error: Hobby '{args.name}' not found", file=sys.stderr)
                return 1
            self.db.delete_hobby(hobby.id)
            print(f"✓ Deleted hobby '{args.name}'")
            return 0
        
        elif args.hobby_command == "stats":
            hobby = self.db.get_hobby_by_name(args.name)
            if not hobby:
                print(f"Error: Hobby '{args.name}' not found", file=sys.stderr)
                return 1
            
            total_expenses = self.db.get_total_expenses(hobby.id)
            total_hours = self.db.get_total_hours(hobby.id)
            expense_per_hour = self.db.get_expense_per_hour(hobby.id)
            
            print(f"\n📊 Statistics for '{hobby.name}'")
            print("=" * 60)
            print(f"Total Expenses:    €{total_expenses:.2f}")
            print(f"Total Hours:       {total_hours:.2f}h")
            if expense_per_hour is not None:
                print(f"💰 Cost per Hour:  €{expense_per_hour:.2f}/h")
            else:
                print(f"💰 Cost per Hour:  N/A (no activities recorded)")
            print()
            return 0
        
        else:
            print("Unknown hobby command", file=sys.stderr)
            return 1
    
    def _handle_expense_command(self, args):
        """Handle expense subcommands."""
        if args.expense_command == "add":
            hobby = self.db.get_hobby_by_name(args.hobby)
            if not hobby:
                print(f"Error: Hobby '{args.hobby}' not found", file=sys.stderr)
                return 1
            
            expense = Expense(
                id=None,
                hobby_id=hobby.id,
                amount=args.amount,
                description=args.description
            )
            expense_id = self.db.add_expense(expense)
            print(f"✓ Added expense of €{args.amount:.2f} to '{args.hobby}' (ID: {expense_id})")
            return 0
        
        elif args.expense_command == "list":
            hobby_id = None
            if args.hobby:
                hobby = self.db.get_hobby_by_name(args.hobby)
                if not hobby:
                    print(f"Error: Hobby '{args.hobby}' not found", file=sys.stderr)
                    return 1
                hobby_id = hobby.id
            
            expenses = self.db.list_expenses(hobby_id)
            if not expenses:
                print("No expenses found.")
                return 0
            
            print("\n💶 Expenses:")
            print("-" * 60)
            for expense in expenses:
                hobby = self.db.get_hobby(expense.hobby_id)
                date_str = expense.date.strftime("%Y-%m-%d")
                print(f"{date_str} | {hobby.name:20s} | €{expense.amount:8.2f}")
                if expense.description:
                    print(f"           {expense.description}")
            print()
            return 0
        
        else:
            print("Unknown expense command", file=sys.stderr)
            return 1
    
    def _handle_activity_command(self, args):
        """Handle activity subcommands."""
        if args.activity_command == "add":
            hobby = self.db.get_hobby_by_name(args.hobby)
            if not hobby:
                print(f"Error: Hobby '{args.hobby}' not found", file=sys.stderr)
                return 1
            
            activity = Activity(
                id=None,
                hobby_id=hobby.id,
                duration_hours=args.hours,
                description=args.description
            )
            activity_id = self.db.add_activity(activity)
            print(f"✓ Added activity of {args.hours:.2f}h to '{args.hobby}' (ID: {activity_id})")
            return 0
        
        elif args.activity_command == "list":
            hobby_id = None
            if args.hobby:
                hobby = self.db.get_hobby_by_name(args.hobby)
                if not hobby:
                    print(f"Error: Hobby '{args.hobby}' not found", file=sys.stderr)
                    return 1
                hobby_id = hobby.id
            
            activities = self.db.list_activities(hobby_id)
            if not activities:
                print("No activities found.")
                return 0
            
            print("\n⏱️  Activities:")
            print("-" * 60)
            for activity in activities:
                hobby = self.db.get_hobby(activity.hobby_id)
                date_str = activity.date.strftime("%Y-%m-%d")
                print(f"{date_str} | {hobby.name:20s} | {activity.duration_hours:6.2f}h")
                if activity.description:
                    print(f"           {activity.description}")
            print()
            return 0
        
        else:
            print("Unknown activity command", file=sys.stderr)
            return 1
    
    def _handle_summary_command(self):
        """Show summary of all hobbies."""
        hobbies = self.db.list_hobbies()
        if not hobbies:
            print("No hobbies found. Add one with 'hobby add <name>'")
            return 0
        
        print("\n" + "=" * 80)
        print(" " * 25 + "📊 HOBBY BUDGET SUMMARY")
        print("=" * 80)
        print()
        
        for hobby in hobbies:
            total_expenses = self.db.get_total_expenses(hobby.id)
            total_hours = self.db.get_total_hours(hobby.id)
            expense_per_hour = self.db.get_expense_per_hour(hobby.id)
            
            print(f"🎯 {hobby.name}")
            print("-" * 80)
            print(f"   Total Expenses:    €{total_expenses:>10.2f}")
            print(f"   Total Hours:       {total_hours:>10.2f}h")
            if expense_per_hour is not None:
                print(f"   💰 Cost per Hour:  €{expense_per_hour:>10.2f}/h")
            else:
                print(f"   💰 Cost per Hour:  {'N/A':>10s}  (no activities recorded)")
            print()
        
        print("=" * 80)
        return 0


def main():
    """Main entry point for CLI."""
    cli = CLI()
    try:
        result = cli.run()
    finally:
        cli.db.close()
    sys.exit(result)


if __name__ == "__main__":
    main()
