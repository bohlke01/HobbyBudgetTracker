# Usage Examples / Verwendungsbeispiele

This document provides practical examples for using the Hobby Budget Tracker application.

Dieses Dokument bietet praktische Beispiele für die Verwendung der Hobby Budget Tracker Anwendung.

## Quick Start / Schnellstart

### Example 1: Tracking Photography Hobby

```bash
# Add the hobby
hobby-budget hobby add "Photography" --description "Taking beautiful photos"

# Add some expenses
hobby-budget expense add "Photography" 299.99 --description "Camera lens"
hobby-budget expense add "Photography" 50.00 --description "Memory card"
hobby-budget expense add "Photography" 15.00 --description "Photo prints"

# Log your activities (time spent in hours)
hobby-budget activity add "Photography" 2.5 --description "Photo walk in park"
hobby-budget activity add "Photography" 3.0 --description "Editing session"
hobby-budget activity add "Photography" 1.5 --description "Learning new techniques"

# View statistics - see your cost per hour!
hobby-budget hobby stats "Photography"
```

**Output:**
```
📊 Statistics for 'Photography'
============================================================
Total Expenses:    €364.99
Total Hours:       7.00h
💰 Cost per Hour:  €52.14/h
```

### Example 2: Comparing Multiple Hobbies

```bash
# Add multiple hobbies
hobby-budget hobby add "Gaming" --description "Video games"
hobby-budget hobby add "Cooking" --description "Trying new recipes"
hobby-budget hobby add "Cycling" --description "Mountain biking"

# Gaming expenses and time
hobby-budget expense add "Gaming" 399.00 --description "Console"
hobby-budget expense add "Gaming" 59.99 --description "New game"
hobby-budget activity add "Gaming" 25.0 --description "Playing time"

# Cooking expenses and time
hobby-budget expense add "Cooking" 120.00 --description "Kitchen equipment"
hobby-budget expense add "Cooking" 45.00 --description "Ingredients"
hobby-budget activity add "Cooking" 12.0 --description "Cooking sessions"

# Cycling expenses and time
hobby-budget expense add "Cycling" 800.00 --description "Mountain bike"
hobby-budget expense add "Cycling" 50.00 --description "Accessories"
hobby-budget activity add "Cycling" 40.0 --description "Rides"

# Compare all hobbies
hobby-budget summary
```

**Output:**
```
================================================================================
                         📊 HOBBY BUDGET SUMMARY
================================================================================

🎯 Cooking
--------------------------------------------------------------------------------
   Total Expenses:    €    165.00
   Total Hours:            12.00h
   💰 Cost per Hour:  €     13.75/h

🎯 Cycling
--------------------------------------------------------------------------------
   Total Expenses:    €    850.00
   Total Hours:            40.00h
   💰 Cost per Hour:  €     21.25/h

🎯 Gaming
--------------------------------------------------------------------------------
   Total Expenses:    €    458.99
   Total Hours:            25.00h
   💰 Cost per Hour:  €     18.36/h

================================================================================
```

### Example 3: Tracking Monthly Progress

```bash
# Week 1
hobby-budget activity add "Photography" 2.0 --description "Week 1: Landscape photography"

# Week 2
hobby-budget activity add "Photography" 3.5 --description "Week 2: Portrait session"
hobby-budget expense add "Photography" 25.00 --description "New tripod"

# Week 3
hobby-budget activity add "Photography" 2.5 --description "Week 3: Editing"

# Week 4
hobby-budget activity add "Photography" 4.0 --description "Week 4: Photo walk"

# Check monthly stats
hobby-budget hobby stats "Photography"
```

### Example 4: Managing Expenses

```bash
# View all expenses across all hobbies
hobby-budget expense list

# View expenses for a specific hobby
hobby-budget expense list --hobby "Gaming"

# Example output:
# 💶 Expenses:
# ------------------------------------------------------------
# 2025-12-17 | Gaming               | €   59.99
#            New game
# 2025-12-15 | Gaming               | €  399.00
#            Console
```

### Example 5: Managing Activities

```bash
# View all activities across all hobbies
hobby-budget activity list

# View activities for a specific hobby
hobby-budget activity list --hobby "Cycling"

# Example output:
# ⏱️  Activities:
# ------------------------------------------------------------
# 2025-12-17 | Cycling              |  10.00h
#            Weekend ride
# 2025-12-15 | Cycling              |   5.00h
#            Evening ride
```

### Example 6: Deleting a Hobby

```bash
# Delete a hobby (this will also delete all related expenses and activities)
hobby-budget hobby delete "OldHobby"

# Output: ✓ Deleted hobby 'OldHobby'
```

## Advanced Use Cases / Erweiterte Anwendungsfälle

### Budget Planning

Use the expense per hour metric to plan your hobby budget:

```bash
# Check your current cost per hour
hobby-budget hobby stats "Gaming"

# If you plan to spend 20 hours next month and your cost per hour is €18.36/h:
# Expected cost: 20h × €18.36/h = €367.20
```

### Finding Your Most Expensive Hobby

```bash
# Run summary and compare the "Cost per Hour" values
hobby-budget summary

# The hobby with the highest €/h value is your most expensive per unit of time
```

### Tracking Equipment Purchases

```bash
# Large one-time purchase
hobby-budget expense add "Photography" 1200.00 --description "Professional camera"

# The cost per hour will be high initially
hobby-budget hobby stats "Photography"

# But as you log more activities, the cost per hour decreases
hobby-budget activity add "Photography" 10.0 --description "Practice session"
hobby-budget hobby stats "Photography"
```

## Tips / Tipps

1. **Be Consistent**: Log activities soon after completing them
2. **Include All Costs**: Don't forget small expenses like supplies or subscriptions
3. **Regular Reviews**: Check your summary monthly to understand spending patterns
4. **Set Goals**: Use the cost per hour to set budget goals for each hobby

---

For more information, see the [README.md](README.md) file.
