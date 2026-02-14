# HobbyBudgetTracker

![Tests and Coverage](https://github.com/bohlke01/HobbyBudgetTracker/actions/workflows/test-coverage.yml/badge.svg)
![Deploy to PythonAnywhere](https://github.com/bohlke01/HobbyBudgetTracker/actions/workflows/deploy-pythonanywhere.yml/badge.svg)

Eine Cross-Platform-Anwendung in Python zum Tracken von Budgets und Aktivitäten für verschiedene Hobbys.

A cross-platform Python application to track budgets and activities for different hobbies.

## Features / Funktionen

- ✅ Track multiple hobbies / Mehrere Hobbys verfolgen
- 💰 Record expenses for each hobby / Ausgaben für jedes Hobby erfassen
- ⏱️ Log activity duration / Aktivitätsdauer protokollieren
- 📊 Calculate key KPI: **Expenses per Hour** / Zentrale KPI berechnen: **Ausgaben pro Stunde**
- 💾 SQLite database for data persistence / SQLite-Datenbank für Datenpersistenz
- 🖥️ Simple command-line interface / Einfache Kommandozeilen-Schnittstelle
- 🌐 **Responsive web interface** / **Responsive Weboberfläche**
- 📱 Mobile-friendly design / Mobilfreundliches Design
- 🌍 Cross-platform (Windows, macOS, Linux) / Plattformübergreifend

## Installation

### Requirements / Voraussetzungen

- Python 3.12

### Install / Installation

```bash
# Clone the repository / Repository klonen
git clone https://github.com/bohlke01/HobbyBudgetTracker.git
cd HobbyBudgetTracker

# Install the package / Paket installieren
pip install -e .

# Or run directly without installation / Oder direkt ausführen ohne Installation
python -m hobby_budget_tracker
```

## Usage / Verwendung

### Web Interface / Weboberfläche (Recommended / Empfohlen)

The easiest way to use Hobby Budget Tracker is through the web interface:

Die einfachste Art, Hobby Budget Tracker zu verwenden, ist über die Weboberfläche:

```bash
# Start the web server / Webserver starten
hobby-budget-web

# Or run directly / Oder direkt ausführen
python -m hobby_budget_tracker.web
```

Then open your browser and navigate to `http://localhost:5000`

Öffnen Sie dann Ihren Browser und navigieren Sie zu `http://localhost:5000`

The web interface features:
- 📊 Dashboard with summary of all hobbies
- ➕ Add and manage hobbies, expenses, and activities
- 📱 Responsive design that works on mobile and desktop
- 🎨 Modern, user-friendly interface

Die Weboberfläche bietet:
- 📊 Dashboard mit Zusammenfassung aller Hobbys
- ➕ Hobbys, Ausgaben und Aktivitäten hinzufügen und verwalten
- 📱 Responsives Design für Mobilgeräte und Desktop
- 🎨 Moderne, benutzerfreundliche Oberfläche

### Command-Line Interface / Kommandozeilen-Schnittstelle

### Managing Hobbies / Hobbys verwalten

```bash
# Add a new hobby / Neues Hobby hinzufügen
hobby-budget hobby add "Photography" --description "Taking photos"

# List all hobbies / Alle Hobbys auflisten
hobby-budget hobby list

# Show statistics for a hobby / Statistiken für ein Hobby anzeigen
hobby-budget hobby stats "Photography"

# Delete a hobby / Hobby löschen
hobby-budget hobby delete "Photography"
```

### Tracking Expenses / Ausgaben erfassen

```bash
# Add an expense / Ausgabe hinzufügen
hobby-budget expense add "Photography" 299.99 --description "New camera lens"

# List all expenses / Alle Ausgaben auflisten
hobby-budget expense list

# List expenses for a specific hobby / Ausgaben für ein bestimmtes Hobby auflisten
hobby-budget expense list --hobby "Photography"
```

### Logging Activities / Aktivitäten protokollieren

```bash
# Add an activity (duration in hours) / Aktivität hinzufügen (Dauer in Stunden)
hobby-budget activity add "Photography" 2.5 --description "Photo walk in the park"

# List all activities / Alle Aktivitäten auflisten
hobby-budget activity list

# List activities for a specific hobby / Aktivitäten für ein bestimmtes Hobby auflisten
hobby-budget activity list --hobby "Photography"
```

### Summary / Zusammenfassung

```bash
# Show summary of all hobbies with KPI / Zusammenfassung aller Hobbys mit KPI anzeigen
hobby-budget summary
```

## Example Workflow / Beispiel-Workflow

```bash
# 1. Add a hobby / Hobby hinzufügen
hobby-budget hobby add "Gaming" --description "Video games"

# 2. Track expenses / Ausgaben erfassen
hobby-budget expense add "Gaming" 59.99 --description "New game"
hobby-budget expense add "Gaming" 399.00 --description "Gaming console"

# 3. Log activities / Aktivitäten protokollieren
hobby-budget activity add "Gaming" 3.5 --description "Played new game"
hobby-budget activity add "Gaming" 2.0 --description "Online multiplayer"

# 4. View statistics / Statistiken ansehen
hobby-budget hobby stats "Gaming"
# Output:
# 📊 Statistics for 'Gaming'
# ============================================================
# Total Expenses:    €458.99
# Total Hours:       5.50h
# 💰 Cost per Hour:  €83.45/h

# 5. View summary of all hobbies / Zusammenfassung aller Hobbys ansehen
hobby-budget summary
```

## Project Structure / Projektstruktur

```
HobbyBudgetTracker/
├── hobby_budget_tracker/
│   ├── __init__.py          # Package initialization
│   ├── __main__.py          # Main entry point
│   ├── models.py            # Data models (Hobby, Expense, Activity)
│   ├── database.py          # SQLite database operations
│   ├── cli.py               # Command-line interface
│   ├── web.py               # Web interface (Flask)
│   └── templates/           # HTML templates
├── tests/
│   ├── __init__.py
│   ├── test_database.py     # Database tests
│   ├── test_cli.py          # CLI tests
│   └── test_web.py          # Web interface tests
├── setup.py                 # Package setup configuration
├── requirements.txt         # Dependencies
└── README.md               # This file
```

## Running Tests / Tests ausführen

```bash
# Run all tests / Alle Tests ausführen
python -m unittest discover tests

# Run specific test file / Bestimmte Test-Datei ausführen
python -m unittest tests.test_database
python -m unittest tests.test_cli
python -m unittest tests.test_web

# Run tests with coverage / Tests mit Coverage ausführen
coverage run -m unittest discover tests
coverage report
coverage html  # Generates htmlcov/index.html / Erzeugt htmlcov/index.html
```

## Database / Datenbank

The application uses SQLite to store data in a file called `hobby_budget.db` in the current directory. The database contains three tables:

Die Anwendung verwendet SQLite zum Speichern von Daten in einer Datei namens `hobby_budget.db` im aktuellen Verzeichnis. Die Datenbank enthält drei Tabellen:

- **hobbies**: Stores hobby information / Speichert Hobby-Informationen
- **expenses**: Stores expense records / Speichert Ausgabendatensätze
- **activities**: Stores activity logs / Speichert Aktivitätsprotokolle

## KPI: Expenses per Hour / KPI: Ausgaben pro Stunde

The central Key Performance Indicator (KPI) is **Expenses per Hour**, calculated as:

Der zentrale Key Performance Indicator (KPI) ist **Ausgaben pro Stunde**, berechnet als:

```
Expenses per Hour = Total Expenses / Total Hours
Ausgaben pro Stunde = Gesamtausgaben / Gesamtstunden
```

This helps you understand how much money you spend per hour of enjoyment for each hobby.

Dies hilft Ihnen zu verstehen, wie viel Geld Sie pro Stunde Vergnügen für jedes Hobby ausgeben.

## Deployment / Bereitstellung

### PythonAnywhere

For detailed instructions on how to deploy this application on PythonAnywhere, see [DEPLOYMENT.md](DEPLOYMENT.md).

Für detaillierte Anweisungen zur Bereitstellung dieser Anwendung auf PythonAnywhere siehe [DEPLOYMENT.md](DEPLOYMENT.md).

#### Continuous Deployment / Kontinuierliche Bereitstellung

This repository includes continuous deployment to PythonAnywhere via GitHub Actions. See [CONTINUOUS_DEPLOYMENT.md](CONTINUOUS_DEPLOYMENT.md) for setup instructions.

Dieses Repository enthält kontinuierliche Bereitstellung zu PythonAnywhere über GitHub Actions. Siehe [CONTINUOUS_DEPLOYMENT.md](CONTINUOUS_DEPLOYMENT.md) für Einrichtungsanweisungen.

## License / Lizenz

This project is licensed under the MIT License - see the LICENSE file for details.

Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe die LICENSE-Datei für Details.