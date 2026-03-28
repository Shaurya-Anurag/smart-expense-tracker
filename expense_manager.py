"""
expense_manager.py
------------------
Handles all CRUD operations for expenses.
Data is stored in a local CSV file — no database required.
"""

import csv
import os
from datetime import datetime

EXPENSES_FILE = "data/expenses.csv"
FIELDNAMES = ["date", "amount", "description", "category"]


def _ensure_file():
    """Create the CSV file with headers if it doesn't exist."""
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(EXPENSES_FILE):
        with open(EXPENSES_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()


def add_expense(amount: float, description: str, category: str) -> dict:
    """
    Append a new expense record to the CSV.
    Returns the saved expense dict.
    """
    _ensure_file()
    record = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "amount": round(amount, 2),
        "description": description,
        "category": category,
    }
    with open(EXPENSES_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow(record)
    return record


def load_expenses() -> list[dict]:
    """
    Load all expenses from CSV.
    Returns a list of dicts; amounts are cast to float.
    """
    _ensure_file()
    expenses = []
    with open(EXPENSES_FILE, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                row["amount"] = float(row["amount"])
                expenses.append(row)
            except (ValueError, KeyError):
                pass  # Skip malformed rows
    return expenses


def delete_all_expenses():
    """Wipe all expense data (used for reset/testing)."""
    _ensure_file()
    with open(EXPENSES_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
