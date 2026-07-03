"""Earnings page for the Nebula Creator Dashboard.

Purpose:
- Show creator earnings, pending payments, completed payments, transaction
  history and provide a withdraw action. Data is sourced from
  `data.dummy_data.get_earnings()` when available, otherwise a fallback is
  generated for the prototype.

Public API:
- `render_page()` - Streamlit callable used by the app router.
"""

from __future__ import annotations

from typing import Any, Dict, List

import streamlit as st

try:
    from data.dummy_data import get_earnings  # type: ignore
except Exception:
    get_earnings = None

import pandas as pd
import plotly.express as px
from datetime import date, timedelta


def _fallback_earnings() -> Dict[str, Any]:
    """Return a simple earnings dataset for the UI prototype.

    Contains totals, a list of transactions, and monthly earnings timeseries.
    """

    months = pd.date_range(end=pd.Timestamp.today(), periods=12, freq="ME").strftime("%b %Y")
    monthly_earnings = pd.Series([1200, 1500, 1700, 1400, 1800, 2200, 2600, 2400, 2700, 3000, 3200, 3500], index=months)

    transactions = [
        {"date": date.today() - timedelta(days=7), "description": "Aurora Labs - final payment", "amount": 1200, "status": "Completed"},
        {"date": date.today() - timedelta(days=20), "description": "PulseAI - milestone 2", "amount": 800, "status": "Completed"},
        {"date": date.today() - timedelta(days=35), "description": "GreenSpark - initial payment", "amount": 600, "status": "Pending"},
    ]

    totals = {"total": int(monthly_earnings.sum()), "pending": 600, "completed": int(monthly_earnings.sum()) - 600}

    return {"totals": totals, "monthly": monthly_earnings, "transactions": transactions}


def render_summary(totals: Dict[str, Any]) -> None:
    """Render top-level earnings summary metrics.

    Uses `st.metric` for a clear, accessible summary presentation.
    """

    st.subheader("Earnings Summary")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Earnings", f"${totals.get('total', 0):,}")
    c2.metric("Pending", f"${totals.get('pending', 0):,}")
    c3.metric("Completed", f"${totals.get('completed', 0):,}")


def render_transactions(transactions: List[Dict[str, Any]]) -> None:
    """Render transaction history in a simple table.

    In a production app this table would support pagination, CSV export and
    invoice links.
    """

    st.subheader("Transaction History")
    df = pd.DataFrame(transactions)
    if not df.empty:
        df["date"] = pd.to_datetime(df["date"]).dt.date
        st.dataframe(df.sort_values(by="date", ascending=False), use_container_width=True)
    else:
        st.write("No transactions yet.")


def render_monthly_chart(monthly: pd.Series) -> None:
    """Render a simple monthly earnings chart using Plotly.

    The chart function is kept here for now but should be moved to
    `components/charts.py` for reuse once multiple pages share charts.
    """

    st.subheader("Monthly Earnings")
    fig = px.area(x=monthly.index, y=monthly.values, labels={"x": "Month", "y": "Earnings ($)"}, title="Monthly Earnings")
    st.plotly_chart(fig, use_container_width=True)


def render_withdraw_section(totals: Dict[str, Any]) -> None:
    """Render a withdraw UI stub. The button is a placeholder — connect to
    a backend payout API to actually move funds.
    """

    st.subheader("Withdraw Funds")
    st.write("Available to withdraw: ", f"${totals.get('pending', 0):,}")
    amount = st.number_input("Amount to withdraw", min_value=0, max_value=totals.get("pending", 0), value=0)
    destination = st.text_input("Destination account (placeholder)")
    if st.button("Withdraw"):
        st.success(f"Withdraw request for ${amount} submitted. Integrate with payments API to process.")


def render_page() -> None:
    """Streamlit entrypoint for the Earnings page.

    Isolates rendering from data acquisition so the same UI can be used with
    dummy data or a remote API later on.
    """

    st.title("Earnings")

    if get_earnings is not None:
        data = get_earnings()
    else:
        st.info("`data/dummy_data.py` not found — using fallback earnings data.")
        data = _fallback_earnings()

    totals = data["totals"]
    monthly = data["monthly"]
    transactions = data["transactions"]

    render_summary(totals)
    render_monthly_chart(monthly)
    render_transactions(transactions)
    st.markdown("---")
    render_withdraw_section(totals)


if __name__ == "__main__":
    render_page()
