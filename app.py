"""
app.py
------
Smart Expense Tracker — Main Streamlit Application
Run with: streamlit run app.py
"""

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from datetime import datetime

import classifier
import expense_manager
import goal_manager
import analyzer

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Smart Expense Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .main {
        background: #0f0f13;
    }

    [data-testid="stSidebar"] {
        background: #16161d;
        border-right: 1px solid #2a2a35;
    }

    .block-container {
        padding-top: 2rem;
        max-width: 1200px;
    }

    h1, h2, h3 {
        font-family: 'Space Mono', monospace !important;
        color: #e8e8f0 !important;
        letter-spacing: -0.5px;
    }

    .stTextInput > div > div > input {
        background: #1e1e2a;
        border: 1px solid #3a3a50;
        border-radius: 8px;
        color: #e8e8f0;
        font-family: 'Space Mono', monospace;
        font-size: 1.05rem;
        padding: 0.75rem 1rem;
    }

    .stTextInput > div > div > input:focus {
        border-color: #7c6fff;
        box-shadow: 0 0 0 2px rgba(124,111,255,0.25);
    }

    .stNumberInput > div > div > input {
        background: #1e1e2a;
        border: 1px solid #3a3a50;
        border-radius: 8px;
        color: #e8e8f0;
    }

    .stButton > button {
        background: linear-gradient(135deg, #7c6fff, #b06fff);
        color: white;
        border: none;
        border-radius: 8px;
        font-family: 'Space Mono', monospace;
        font-weight: 700;
        font-size: 0.85rem;
        letter-spacing: 0.5px;
        padding: 0.6rem 1.5rem;
        width: 100%;
        transition: all 0.2s;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 20px rgba(124,111,255,0.4);
    }

    .metric-card {
        background: #1a1a24;
        border: 1px solid #2a2a38;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 0.8rem;
    }

    .metric-label {
        color: #6b6b88;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
        margin-bottom: 0.3rem;
    }

    .metric-value {
        color: #7c6fff;
        font-family: 'Space Mono', monospace;
        font-size: 1.6rem;
        font-weight: 700;
    }

    .expense-row {
        background: #1a1a24;
        border: 1px solid #2a2a38;
        border-radius: 10px;
        padding: 0.8rem 1.2rem;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
    }

    .category-pill {
        display: inline-block;
        padding: 0.2rem 0.7rem;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }

    .alert-box {
        background: #1f1a2e;
        border-left: 3px solid #7c6fff;
        border-radius: 0 8px 8px 0;
        padding: 0.8rem 1rem;
        margin: 0.4rem 0;
        color: #d0cfea;
        font-size: 0.9rem;
    }

    .success-box {
        background: #1a2e1f;
        border-left: 3px solid #4caf7d;
        border-radius: 0 8px 8px 0;
        padding: 0.8rem 1rem;
        margin: 0.4rem 0;
        color: #b5e0c4;
        font-size: 0.9rem;
    }

    .section-title {
        font-family: 'Space Mono', monospace;
        font-size: 0.7rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #5a5a75;
        margin-bottom: 1rem;
        border-bottom: 1px solid #2a2a38;
        padding-bottom: 0.5rem;
    }

    .hint-text {
        color: #4a4a60;
        font-size: 0.78rem;
        margin-top: 0.3rem;
    }

    div[data-testid="stSelectbox"] > div {
        background: #1e1e2a;
        border: 1px solid #3a3a50;
        border-radius: 8px;
        color: #e8e8f0;
    }

    .stMarkdown p {
        color: #b0b0c8;
    }

    [data-testid="metric-container"] {
        background: #1a1a24;
        border: 1px solid #2a2a38;
        border-radius: 10px;
        padding: 1rem;
    }

    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  CATEGORY COLOR MAP
# ─────────────────────────────────────────────
CATEGORY_COLORS = {
    "Food":          "#ff7eb3",
    "Transport":     "#7eb3ff",
    "Entertainment": "#ffb37e",
    "Essentials":    "#7effc5",
    "Shopping":      "#d17eff",
    "Other":         "#aaaacc",
}

CATEGORY_EMOJIS = {
    "Food": "🍜",
    "Transport": "🚗",
    "Entertainment": "🎬",
    "Essentials": "🏠",
    "Shopping": "🛍️",
    "Other": "📦",
}


def category_color(cat):
    return CATEGORY_COLORS.get(cat, "#aaaacc")


# ─────────────────────────────────────────────
#  SIDEBAR — NAVIGATION
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 💰 ExpenseIQ")
    st.markdown('<p style="color:#5a5a75;font-size:0.8rem;margin-top:-0.5rem;">Smart Expense Tracker</p>', unsafe_allow_html=True)
    st.markdown("---")

    page = st.radio(
        "Navigate",
        ["📥 Add Expense", "🎯 Set Goal", "📊 Analysis", "🗂️ All Expenses"],
        label_visibility="collapsed"
    )

    st.markdown("---")

    # Quick stats in sidebar
    all_expenses = expense_manager.load_expenses()
    st.markdown('<div class="section-title">Quick Stats</div>', unsafe_allow_html=True)

    total = analyzer.total_spending(all_expenses)
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Spent</div>
        <div class="metric-value">₹{total:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

    monthly = analyzer.current_month_expenses(all_expenses)
    monthly_total = analyzer.total_spending(monthly)
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">This Month</div>
        <div class="metric-value">₹{monthly_total:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

    goal = goal_manager.get_active_goal()
    if goal:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Active Goal</div>
            <div class="metric-value" style="font-size:1.1rem;">{goal['name']}</div>
            <div style="color:#5a5a75;font-size:0.78rem;margin-top:0.2rem;">₹{goal['target_amount']:,.0f} in {goal['months']}mo</div>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  PAGE 1: ADD EXPENSE
# ─────────────────────────────────────────────
if page == "📥 Add Expense":
    st.markdown("## Add Expense")
    st.markdown('<div class="section-title">Smart Input Parser</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])

    with col1:
        user_input = st.text_input(
            "Expense",
            placeholder="e.g.  250 swiggy  |  1200 uber  |  800 netflix subscription",
            label_visibility="collapsed"
        )
        st.markdown('<p class="hint-text">Type: [amount] [description] — the AI will classify it automatically</p>', unsafe_allow_html=True)

    with col2:
        add_clicked = st.button("➕ Add", use_container_width=True)

    # Live preview
    if user_input:
        parsed = classifier.parse_expense(user_input)
        if parsed:
            color = category_color(parsed["category"])
            emoji = CATEGORY_EMOJIS.get(parsed["category"], "📦")
            st.markdown(f"""
            <div style="background:#1a1a24;border:1px solid {color}33;border-radius:12px;padding:1rem 1.5rem;margin-top:0.5rem;">
                <span style="color:#5a5a75;font-size:0.72rem;text-transform:uppercase;letter-spacing:1.5px;">Preview</span><br>
                <span style="color:#e8e8f0;font-size:1.1rem;font-weight:600;">₹{parsed['amount']:,.2f}</span>
                <span style="color:#b0b0c8;margin:0 0.5rem;">—</span>
                <span style="color:#e8e8f0;">{parsed['description']}</span>
                <span style="background:{color}22;color:{color};padding:0.2rem 0.7rem;border-radius:20px;font-size:0.72rem;font-weight:600;letter-spacing:0.5px;text-transform:uppercase;margin-left:0.5rem;">{emoji} {parsed['category']}</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Could not parse. Try: `350 zomato biryani`")

    if add_clicked:
        if not user_input:
            st.error("Please enter an expense.")
        else:
            parsed = classifier.parse_expense(user_input)
            if not parsed:
                st.error("Invalid format. Use: `[amount] [description]` e.g. `250 swiggy`")
            else:
                expense_manager.add_expense(
                    parsed["amount"], parsed["description"], parsed["category"]
                )
                color = category_color(parsed["category"])
                emoji = CATEGORY_EMOJIS.get(parsed["category"], "📦")
                st.success(f"✅ Saved! ₹{parsed['amount']:,.2f} — {parsed['description']} → {emoji} {parsed['category']}")
                st.balloons()

    # Recent expenses
    st.markdown("---")
    st.markdown('<div class="section-title">Recent Expenses</div>', unsafe_allow_html=True)

    expenses = expense_manager.load_expenses()
    if not expenses:
        st.markdown('<p style="color:#4a4a60;text-align:center;padding:2rem;">No expenses yet. Add your first one above!</p>', unsafe_allow_html=True)
    else:
        for e in reversed(expenses[-10:]):
            color = category_color(e["category"])
            emoji = CATEGORY_EMOJIS.get(e["category"], "📦")
            st.markdown(f"""
            <div style="background:#1a1a24;border:1px solid #2a2a38;border-radius:10px;padding:0.75rem 1.2rem;margin-bottom:0.4rem;display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <span style="color:#e8e8f0;font-weight:500;">{e['description']}</span>
                    <span style="background:{color}22;color:{color};padding:0.15rem 0.6rem;border-radius:20px;font-size:0.68rem;font-weight:600;text-transform:uppercase;margin-left:0.5rem;">{emoji} {e['category']}</span>
                </div>
                <div style="text-align:right;">
                    <span style="color:#7c6fff;font-family:'Space Mono',monospace;font-weight:700;">₹{e['amount']:,.2f}</span>
                    <span style="color:#4a4a60;font-size:0.78rem;margin-left:0.7rem;">{e['date']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  PAGE 2: SET GOAL
# ─────────────────────────────────────────────
elif page == "🎯 Set Goal":
    st.markdown("## Set Financial Goal")
    st.markdown('<div class="section-title">Define Your Saving Target</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        goal_name = st.text_input("Goal Name", placeholder="e.g. New Laptop, Vacation, Emergency Fund")
    with col2:
        goal_amount = st.number_input("Target Amount (₹)", min_value=100.0, value=10000.0, step=500.0)
    with col3:
        goal_months = st.number_input("Timeframe (months)", min_value=1, max_value=120, value=6)

    if st.button("🎯 Set Goal", use_container_width=True):
        if not goal_name.strip():
            st.error("Please enter a goal name.")
        else:
            try:
                saved = goal_manager.add_goal(goal_name, goal_amount, int(goal_months))
                st.success(f"✅ Goal set! Save **₹{saved['monthly_saving']:,.2f}/month** for **{int(goal_months)} months** to reach **₹{goal_amount:,.2f}**.")
            except ValueError as e:
                st.error(str(e))

    # Show all goals
    st.markdown("---")
    st.markdown('<div class="section-title">Your Goals</div>', unsafe_allow_html=True)
    goals = goal_manager.load_goals()

    if not goals:
        st.markdown('<p style="color:#4a4a60;text-align:center;padding:2rem;">No goals set yet.</p>', unsafe_allow_html=True)
    else:
        for g in reversed(goals):
            progress_pct = min(100, (analyzer.total_spending(analyzer.current_month_expenses(expense_manager.load_expenses())) / g["monthly_saving"]) * 100) if g["monthly_saving"] > 0 else 0
            st.markdown(f"""
            <div style="background:#1a1a24;border:1px solid #2a2a38;border-radius:12px;padding:1.2rem 1.5rem;margin-bottom:0.8rem;">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                    <div>
                        <div style="color:#e8e8f0;font-size:1.1rem;font-weight:600;font-family:'Space Mono',monospace;">🎯 {g['name']}</div>
                        <div style="color:#5a5a75;font-size:0.8rem;margin-top:0.3rem;">Target: ₹{g['target_amount']:,.2f} · {g['months']} months</div>
                    </div>
                    <div style="text-align:right;">
                        <div style="color:#7c6fff;font-family:'Space Mono',monospace;font-size:1.3rem;font-weight:700;">₹{g['monthly_saving']:,.0f}</div>
                        <div style="color:#5a5a75;font-size:0.72rem;">per month</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            col_del, _ = st.columns([1, 5])
            with col_del:
                if st.button(f"🗑️ Delete", key=f"del_{g['name']}"):
                    goal_manager.delete_goal(g["name"])
                    st.rerun()


# ─────────────────────────────────────────────
#  PAGE 3: ANALYSIS
# ─────────────────────────────────────────────
elif page == "📊 Analysis":
    st.markdown("## Spending Analysis")

    expenses = expense_manager.load_expenses()

    if not expenses:
        st.markdown('<p style="color:#4a4a60;text-align:center;padding:3rem;">Add some expenses first to see analysis!</p>', unsafe_allow_html=True)
    else:
        summary = analyzer.full_summary(expenses)

        # KPIs
        k1, k2, k3, k4 = st.columns(4)
        kpi_style = "background:#1a1a24;border:1px solid #2a2a38;border-radius:12px;padding:1rem 1.2rem;text-align:center;"

        with k1:
            st.markdown(f"""<div style="{kpi_style}">
                <div style="color:#5a5a75;font-size:0.7rem;text-transform:uppercase;letter-spacing:1.5px;">Total Spent</div>
                <div style="color:#7c6fff;font-family:'Space Mono',monospace;font-size:1.5rem;font-weight:700;">₹{summary['total_spending']:,.0f}</div>
            </div>""", unsafe_allow_html=True)
        with k2:
            st.markdown(f"""<div style="{kpi_style}">
                <div style="color:#5a5a75;font-size:0.7rem;text-transform:uppercase;letter-spacing:1.5px;">Avg per Expense</div>
                <div style="color:#ff7eb3;font-family:'Space Mono',monospace;font-size:1.5rem;font-weight:700;">₹{summary['average_spending']:,.0f}</div>
            </div>""", unsafe_allow_html=True)
        with k3:
            st.markdown(f"""<div style="{kpi_style}">
                <div style="color:#5a5a75;font-size:0.7rem;text-transform:uppercase;letter-spacing:1.5px;">Total Entries</div>
                <div style="color:#7effc5;font-family:'Space Mono',monospace;font-size:1.5rem;font-weight:700;">{summary['total_expenses']}</div>
            </div>""", unsafe_allow_html=True)
        with k4:
            top_cat = summary['highest_category'] or "—"
            top_emoji = CATEGORY_EMOJIS.get(top_cat, "📦")
            st.markdown(f"""<div style="{kpi_style}">
                <div style="color:#5a5a75;font-size:0.7rem;text-transform:uppercase;letter-spacing:1.5px;">Top Category</div>
                <div style="color:#ffb37e;font-family:'Space Mono',monospace;font-size:1.3rem;font-weight:700;">{top_emoji} {top_cat}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Charts
        col_pie, col_bar = st.columns(2)

        with col_pie:
            st.markdown('<div class="section-title">Category Breakdown</div>', unsafe_allow_html=True)
            breakdown = summary["category_breakdown"]
            if breakdown:
                fig, ax = plt.subplots(figsize=(5, 5), facecolor="#0f0f13")
                ax.set_facecolor("#0f0f13")

                labels = list(breakdown.keys())
                values = list(breakdown.values())
                colors = [category_color(c) for c in labels]

                wedges, texts, autotexts = ax.pie(
                    values,
                    labels=None,
                    colors=colors,
                    autopct="%1.0f%%",
                    startangle=90,
                    pctdistance=0.78,
                    wedgeprops=dict(width=0.55, edgecolor="#0f0f13", linewidth=2),
                )
                for at in autotexts:
                    at.set_color("#e8e8f0")
                    at.set_fontsize(10)
                    at.set_fontweight("bold")

                legend_patches = [mpatches.Patch(color=colors[i], label=f"{labels[i]}  ₹{values[i]:,.0f}") for i in range(len(labels))]
                ax.legend(handles=legend_patches, loc="lower center", bbox_to_anchor=(0.5, -0.18),
                          ncol=2, frameon=False, fontsize=9,
                          labelcolor="#b0b0c8")

                ax.set_title("Spending by Category", color="#e8e8f0", fontsize=12, pad=15, fontweight="bold")
                st.pyplot(fig)
                plt.close()

        with col_bar:
            st.markdown('<div class="section-title">Category Bar Chart</div>', unsafe_allow_html=True)
            if breakdown:
                fig2, ax2 = plt.subplots(figsize=(5, 5), facecolor="#0f0f13")
                ax2.set_facecolor("#1a1a24")

                cats = list(breakdown.keys())
                amts = list(breakdown.values())
                bar_colors = [category_color(c) for c in cats]

                bars = ax2.barh(cats, amts, color=bar_colors, height=0.55, edgecolor="none")

                # Value labels
                for bar, amt in zip(bars, amts):
                    ax2.text(bar.get_width() + max(amts) * 0.02, bar.get_y() + bar.get_height() / 2,
                             f"₹{amt:,.0f}", va="center", ha="left",
                             color="#e8e8f0", fontsize=9, fontweight="bold")

                ax2.set_xlabel("Amount (₹)", color="#5a5a75", fontsize=9)
                ax2.tick_params(colors="#b0b0c8", labelsize=10)
                ax2.spines[:].set_color("#2a2a38")
                ax2.xaxis.label.set_color("#5a5a75")
                ax2.set_xlim(0, max(amts) * 1.25)
                ax2.set_title("Amount by Category", color="#e8e8f0", fontsize=12, pad=12, fontweight="bold")
                fig2.tight_layout()
                st.pyplot(fig2)
                plt.close()

        # Daily trend
        st.markdown("---")
        st.markdown('<div class="section-title">Daily Spending Trend</div>', unsafe_allow_html=True)
        daily = summary["daily_trend"]

        if len(daily) >= 2:
            fig3, ax3 = plt.subplots(figsize=(10, 3.5), facecolor="#0f0f13")
            ax3.set_facecolor("#1a1a24")
            dates = list(daily.keys())
            amounts = list(daily.values())

            ax3.fill_between(dates, amounts, alpha=0.15, color="#7c6fff")
            ax3.plot(dates, amounts, color="#7c6fff", linewidth=2.5, marker="o",
                     markersize=5, markerfacecolor="#7c6fff", markeredgecolor="#0f0f13", markeredgewidth=2)

            ax3.set_ylabel("Amount (₹)", color="#5a5a75", fontsize=9)
            ax3.tick_params(colors="#b0b0c8", labelsize=8)
            ax3.spines[:].set_color("#2a2a38")

            if len(dates) > 7:
                step = max(1, len(dates) // 7)
                ax3.set_xticks(range(0, len(dates), step))
                ax3.set_xticklabels([dates[i] for i in range(0, len(dates), step)], rotation=30)

            ax3.set_title("Daily Spending Over Time", color="#e8e8f0", fontsize=11, pad=10)
            fig3.tight_layout()
            st.pyplot(fig3)
            plt.close()
        else:
            st.markdown('<p style="color:#4a4a60;">Add more expenses over different days to see the trend.</p>', unsafe_allow_html=True)

        # Goal analysis
        goal = goal_manager.get_active_goal()
        if goal:
            st.markdown("---")
            st.markdown('<div class="section-title">Goal Analysis</div>', unsafe_allow_html=True)
            ga = analyzer.goal_analysis(expenses, goal)

            col_ga1, col_ga2 = st.columns(2)
            with col_ga1:
                st.markdown(f"""
                <div style="background:#1a1a24;border:1px solid #2a2a38;border-radius:12px;padding:1.2rem 1.5rem;">
                    <div style="color:#5a5a75;font-size:0.72rem;text-transform:uppercase;letter-spacing:1.5px;">Goal</div>
                    <div style="color:#e8e8f0;font-size:1.2rem;font-weight:600;font-family:'Space Mono',monospace;margin-top:0.2rem;">🎯 {ga['goal_name']}</div>
                    <div style="color:#7c6fff;font-size:1.5rem;font-weight:700;font-family:'Space Mono',monospace;margin-top:0.5rem;">₹{ga['target_amount']:,.0f}</div>
                    <div style="color:#5a5a75;font-size:0.8rem;margin-top:0.2rem;">Save ₹{ga['monthly_saving_required']:,.0f}/month</div>
                </div>
                """, unsafe_allow_html=True)
            with col_ga2:
                status_color = "#4caf7d" if ga["on_track"] else "#ff6b6b"
                status_text = "ON TRACK ✅" if ga["on_track"] else "AT RISK ⚠️"
                st.markdown(f"""
                <div style="background:#1a1a24;border:1px solid #2a2a38;border-radius:12px;padding:1.2rem 1.5rem;">
                    <div style="color:#5a5a75;font-size:0.72rem;text-transform:uppercase;letter-spacing:1.5px;">This Month</div>
                    <div style="color:#ff7eb3;font-size:1.5rem;font-weight:700;font-family:'Space Mono',monospace;margin-top:0.2rem;">₹{ga['spent_this_month']:,.0f}</div>
                    <div style="color:{status_color};font-size:0.85rem;font-weight:600;margin-top:0.5rem;">{status_text}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            for alert in ga["alerts"]:
                if "✅" in alert:
                    st.markdown(f'<div class="success-box">{alert}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="alert-box">{alert}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:#4a4a60;">Set a financial goal to see goal-based analysis and alerts.</p>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  PAGE 4: ALL EXPENSES
# ─────────────────────────────────────────────
elif page == "🗂️ All Expenses":
    st.markdown("## All Expenses")

    expenses = expense_manager.load_expenses()

    if not expenses:
        st.markdown('<p style="color:#4a4a60;text-align:center;padding:3rem;">No expenses recorded yet.</p>', unsafe_allow_html=True)
    else:
        # Filter controls
        col_f1, col_f2, col_f3 = st.columns(3)
        all_cats = sorted(set(e["category"] for e in expenses))

        with col_f1:
            cat_filter = st.selectbox("Filter by Category", ["All"] + all_cats)
        with col_f2:
            sort_by = st.selectbox("Sort by", ["Date (Newest)", "Date (Oldest)", "Amount (High→Low)", "Amount (Low→High)"])
        with col_f3:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🗑️ Clear ALL Data", use_container_width=True):
                expense_manager.delete_all_expenses()
                st.rerun()

        # Apply filters
        filtered = expenses if cat_filter == "All" else [e for e in expenses if e["category"] == cat_filter]

        if sort_by == "Date (Newest)":
            filtered = sorted(filtered, key=lambda x: x["date"], reverse=True)
        elif sort_by == "Date (Oldest)":
            filtered = sorted(filtered, key=lambda x: x["date"])
        elif sort_by == "Amount (High→Low)":
            filtered = sorted(filtered, key=lambda x: x["amount"], reverse=True)
        else:
            filtered = sorted(filtered, key=lambda x: x["amount"])

        st.markdown(f'<p style="color:#5a5a75;font-size:0.8rem;">{len(filtered)} records</p>', unsafe_allow_html=True)

        for e in filtered:
            color = category_color(e["category"])
            emoji = CATEGORY_EMOJIS.get(e["category"], "📦")
            st.markdown(f"""
            <div style="background:#1a1a24;border:1px solid #2a2a38;border-radius:10px;padding:0.75rem 1.2rem;margin-bottom:0.35rem;display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <span style="color:#e8e8f0;font-weight:500;">{e['description']}</span>
                    <span style="background:{color}22;color:{color};padding:0.15rem 0.6rem;border-radius:20px;font-size:0.68rem;font-weight:600;text-transform:uppercase;margin-left:0.5rem;">{emoji} {e['category']}</span>
                </div>
                <div>
                    <span style="color:#7c6fff;font-family:'Space Mono',monospace;font-weight:700;">₹{e['amount']:,.2f}</span>
                    <span style="color:#4a4a60;font-size:0.78rem;margin-left:0.8rem;">{e['date']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
