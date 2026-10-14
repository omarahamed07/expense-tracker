# CLI Expense Tracker

A command-line app to track personal expenses, built with Python and SQLite.

## Features
- Add, list, and delete expenses
- Filter by category and month
- Spending summary with per-category breakdown
- Input validation and unit tests (pytest)

## Setup
```bash
git clone https://github.com/<your-username>/expense-tracker.git
cd expense-tracker
python -m venv venv
venv\Scripts\activate
```

## Usage
```bash
python main.py add 250 --category food --note "lunch"
python main.py list --month 2026-10
python main.py summary
python main.py delete 3
```

## Run tests
```bash
pip install pytest
pytest
```

## Tech
Python, SQLite, argparse, pytest