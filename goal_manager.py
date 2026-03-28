"""
goal_manager.py
---------------
Manages financial goals.
Stores goals in a JSON file and calculates saving requirements.
"""

import json
import os

GOALS_FILE = "data/goals.json"


def _load_raw() -> list:
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(GOALS_FILE):
        return []
    with open(GOALS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def _save_raw(goals: list):
    os.makedirs("data", exist_ok=True)
    with open(GOALS_FILE, "w") as f:
        json.dump(goals, f, indent=2)


def add_goal(name: str, target_amount: float, months: int) -> dict:
    """
    Save a new financial goal.

    Args:
        name          : e.g. "Laptop", "Vacation"
        target_amount : total money needed (₹)
        months        : time horizon in months

    Returns the goal dict including monthly_saving.
    """
    if months <= 0:
        raise ValueError("Months must be a positive integer.")
    if target_amount <= 0:
        raise ValueError("Target amount must be positive.")

    monthly_saving = round(target_amount / months, 2)
    goal = {
        "name": name.strip().title(),
        "target_amount": round(target_amount, 2),
        "months": months,
        "monthly_saving": monthly_saving,
    }
    goals = _load_raw()
    # Replace existing goal with same name
    goals = [g for g in goals if g["name"].lower() != goal["name"].lower()]
    goals.append(goal)
    _save_raw(goals)
    return goal


def load_goals() -> list[dict]:
    """Return all saved goals."""
    return _load_raw()


def get_active_goal() -> dict | None:
    """Return the most recently added goal (last in list)."""
    goals = _load_raw()
    return goals[-1] if goals else None


def delete_goal(name: str) -> bool:
    """Remove a goal by name. Returns True if found and deleted."""
    goals = _load_raw()
    new_goals = [g for g in goals if g["name"].lower() != name.lower()]
    if len(new_goals) == len(goals):
        return False
    _save_raw(new_goals)
    return True
