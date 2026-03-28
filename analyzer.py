"""
analyzer.py
-----------
Statistical analysis engine for expenses.
Demonstrates: mean, totals, category breakdown, trend detection.
AI concept: rule-based decision system for alerts.
"""

from collections import defaultdict
from datetime import datetime, date
import calendar


# ─────────────────────────────────────────────
#  CORE STATISTICS
# ─────────────────────────────────────────────

def total_spending(expenses: list) -> float:
    """Sum of all expense amounts."""
    return round(sum(e["amount"] for e in expenses), 2)


def average_spending(expenses: list) -> float:
    """Mean expense amount."""
    if not expenses:
        return 0.0
    return round(total_spending(expenses) / len(expenses), 2)


def category_breakdown(expenses: list) -> dict:
    """
    Returns {category: total_amount} sorted descending by amount.
    """
    totals = defaultdict(float)
    for e in expenses:
        totals[e["category"]] += e["amount"]
    # Round values and sort
    return dict(sorted(
        {k: round(v, 2) for k, v in totals.items()}.items(),
        key=lambda x: x[1],
        reverse=True
    ))


def highest_category(expenses: list) -> tuple[str, float] | tuple[None, None]:
    """Returns (category_name, amount) for the highest spending category."""
    breakdown = category_breakdown(expenses)
    if not breakdown:
        return None, None
    top = next(iter(breakdown))
    return top, breakdown[top]


def spending_by_date(expenses: list) -> dict:
    """Returns {date_str: total_amount} for all recorded dates."""
    daily = defaultdict(float)
    for e in expenses:
        daily[e["date"]] += e["amount"]
    return dict(sorted(daily.items()))


def current_month_expenses(expenses: list) -> list:
    """Filter expenses to the current calendar month."""
    now = date.today()
    return [
        e for e in expenses
        if _parse_date(e["date"]).year == now.year
        and _parse_date(e["date"]).month == now.month
    ]


def _parse_date(date_str: str) -> date:
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return date.today()


# ─────────────────────────────────────────────
#  GOAL ANALYSIS  (rule-based AI agent)
# ─────────────────────────────────────────────

def days_left_in_month() -> int:
    today = date.today()
    last_day = calendar.monthrange(today.year, today.month)[1]
    return last_day - today.day


def goal_analysis(expenses: list, goal: dict) -> dict:
    """
    Rule-based decision system:
    - Determines if spending is on track for the goal
    - Generates alerts if overspending is detected

    Returns a dict with analysis results and alert messages.
    """
    monthly_expenses = current_month_expenses(expenses)
    spent_this_month = total_spending(monthly_expenses)
    required_saving = goal["monthly_saving"]

    # Estimate monthly income implied by goal (we don't track income directly)
    # Instead: alert if spending > some fraction indicating risk
    days_elapsed = date.today().day
    total_days = calendar.monthrange(date.today().year, date.today().month)[1]

    # Pro-rated spending limit so far this month
    prorated_limit = (days_elapsed / total_days) * (goal["target_amount"] - required_saving)

    on_track = spent_this_month <= prorated_limit
    surplus_or_deficit = round(prorated_limit - spent_this_month, 2)

    alerts = []

    # Rule 1: Overspending alert
    if not on_track:
        alerts.append(
            f"⚠️  You've spent ₹{spent_this_month:,.0f} this month. "
            f"At this rate, you may not save ₹{required_saving:,.0f}/month for your goal."
        )

    # Rule 2: On track confirmation
    else:
        alerts.append(
            f"✅ Great! You're on track. Estimated surplus this month: ₹{surplus_or_deficit:,.0f}."
        )

    # Rule 3: High single-category spending
    breakdown = category_breakdown(monthly_expenses)
    for cat, amt in breakdown.items():
        if amt > required_saving * 0.5:
            alerts.append(
                f"🔔 '{cat}' spending (₹{amt:,.0f}) is more than 50% of your monthly saving target."
            )

    return {
        "goal_name": goal["name"],
        "target_amount": goal["target_amount"],
        "monthly_saving_required": required_saving,
        "months_remaining": goal["months"],
        "spent_this_month": round(spent_this_month, 2),
        "on_track": on_track,
        "alerts": alerts,
    }


# ─────────────────────────────────────────────
#  SUMMARY REPORT
# ─────────────────────────────────────────────

def full_summary(expenses: list) -> dict:
    """
    Returns a complete statistical summary dictionary.
    """
    cat_top, cat_top_amt = highest_category(expenses)
    return {
        "total_expenses": len(expenses),
        "total_spending": total_spending(expenses),
        "average_spending": average_spending(expenses),
        "category_breakdown": category_breakdown(expenses),
        "highest_category": cat_top,
        "highest_category_amount": cat_top_amt,
        "daily_trend": spending_by_date(expenses),
    }
