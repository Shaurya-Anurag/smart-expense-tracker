# 💰 Smart Expense Tracker with Goal-Based Spending Analysis

A beginner-friendly AI/ML project that tracks expenses, classifies them automatically using rule-based AI, performs statistical analysis, and helps users achieve financial goals.

📄 Project Report: [Project_Report.pdf](./Project_Report.pdf)

---

## 📁 Project Structure

```
smart_expense_tracker/
│
├── app.py              # Main Streamlit UI (entry point)
├── classifier.py       # Rule-based expense classifier (AI concept)
├── expense_manager.py  # CRUD operations — reads/writes expenses.csv
├── goal_manager.py     # Goal CRUD — reads/writes goals.json
├── analyzer.py         # Statistical analysis + rule-based alert system
├── requirements.txt    # Python dependencies
├── README.md           # This file
│
└── data/               # Auto-created at runtime
    ├── expenses.csv    # All expense records
    └── goals.json      # All financial goals
```

---

## ⚙️ Setup & Installation

### Step 1 — Install Python (if not already)
Download Python 3.10+ from https://python.org

### Step 2 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Run the app
```bash
streamlit run app.py
```

The app opens automatically at: **http://localhost:8501**

---

## 🧠 AI/ML Concepts Demonstrated

| Concept | Where |
|---|---|
| **Classification** | `classifier.py` — keyword-based category assignment |
| **Statistical Analysis** | `analyzer.py` — mean, totals, category breakdown |
| **Rule-Based AI Agent** | `analyzer.py → goal_analysis()` — alert generation |
| **Bag-of-Words intuition** | Keyword scoring in `classify()` function |

---

## 💡 Example Inputs

| Input | Parsed As |
|---|---|
| `250 swiggy` | ₹250 — Food |
| `1200 uber airport` | ₹1200 — Transport |
| `499 netflix` | ₹499 — Entertainment |
| `15000 rent june` | ₹15000 — Essentials |
| `3500 amazon laptop bag` | ₹3500 — Shopping |
| `80 chai` | ₹80 — Food |

---

## 🎯 Example Goal

| Field | Value |
|---|---|
| Goal Name | New Laptop |
| Target Amount | ₹60,000 |
| Timeframe | 6 months |
| **Monthly Saving Required** | **₹10,000/month** |

---

## 📊 Analysis Features

- **Total spending** — sum of all expenses
- **Average spending** — mean per transaction
- **Category breakdown** — pie + bar chart
- **Daily trend** — line chart over time
- **Goal tracking** — pro-rated monthly check
- **Smart alerts** — warns if spending threatens goal

---

## 🔑 Key Design Decisions

- **No database** — CSV and JSON keep it simple and portable
- **No ML framework** — pure Python + rule-based logic
- **Modular** — each file has one job
- **Beginner-friendly** — every function is commented
