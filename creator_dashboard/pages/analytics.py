"""Analytics page for the Nebula Creator Dashboard.

Purpose:
- Provide rich visualizations for followers growth, reach, impressions,
  engagement metrics, audience demographics, and monthly performance.

Public API:
- `render_page()` - Streamlit entrypoint used by the app router.

Notes:
- Charts use Plotly for interactivity. Data comes from
  `data.dummy_data.get_analytics_data()` when available; otherwise the page
  synthesizes reasonable-looking demo data.
"""

from __future__ import annotations

from typing import Any, Dict

import streamlit as st

try:
    from data.dummy_data import get_analytics_data  # type: ignore
except Exception:
    get_analytics_data = None

import pandas as pd
import numpy as np
import plotly.express as px


def _fallback_analytics() -> Dict[str, Any]:
    """Create fallback analytics datasets for the prototype.

    Returns a dict with timeseries and demographic breakdowns.
    """

    months = pd.date_range(end=pd.Timestamp.today(), periods=12, freq="ME").strftime("%b %Y")
    followers = (np.cumsum(np.random.randint(200, 2000, size=12)) + 20000).astype(int)
    reach = (np.cumsum(np.random.randint(500, 5000, size=12)) + 50000).astype(int)
    impressions = (reach * np.random.uniform(2.5, 4.0, size=12)).astype(int)
    engagement = (np.random.uniform(1.0, 5.0, size=12)).round(2)

    demographics = pd.DataFrame(
        {
            "age_group": ["18-24", "25-34", "35-44", "45-54", "55+"],
            "percent": [28, 40, 18, 8, 6],
        }
    )

    monthly = pd.DataFrame({"month": months, "followers": followers, "reach": reach, "impressions": impressions, "engagement": engagement})

    return {"monthly": monthly, "demographics": demographics}


def render_page() -> None:
    """Render the analytics dashboard page.

    The page organizes charts into logical sections and keeps the underlying
    data acquisition separate so a backend can replace the dummy provider.
    """

    st.title("Analytics")

    if get_analytics_data is not None:
        data = get_analytics_data()
    else:
        st.info("`data/dummy_data.py` not found — using fallback analytics data.")
        data = _fallback_analytics()

    monthly = data["monthly"]
    demographics = data["demographics"]

    # Followers growth
    st.subheader("Followers Growth")
    fig_follow = px.line(monthly, x="month", y="followers", title="Followers Over Time", markers=True)
    fig_follow.update_layout(xaxis_title=None, yaxis_title="Followers")
    st.plotly_chart(fig_follow, use_container_width=True)

    # Reach and impressions side-by-side
    st.subheader("Reach & Impressions")
    c1, c2 = st.columns(2)
    fig_reach = px.line(monthly, x="month", y="reach", title="Reach", markers=True)
    c1.plotly_chart(fig_reach, use_container_width=True)
    fig_impr = px.bar(monthly, x="month", y="impressions", title="Impressions")
    c2.plotly_chart(fig_impr, use_container_width=True)

    # Engagement metrics
    st.subheader("Engagement")
    fig_eng = px.area(monthly, x="month", y="engagement", title="Engagement Rate (%)")
    st.plotly_chart(fig_eng, use_container_width=True)

    # Audience demographics
    st.subheader("Audience Demographics")
    fig_demo = px.pie(demographics, names="age_group", values="percent", title="Age Distribution")
    st.plotly_chart(fig_demo, use_container_width=True)

    # Monthly performance quick table
    st.subheader("Monthly Performance")
    st.dataframe(monthly.style.format({"followers": "{:,}", "reach": "{:,}", "impressions": "{:,}", "engagement": "{:.2f}"}), use_container_width=True)


if __name__ == "__main__":
    render_page()
