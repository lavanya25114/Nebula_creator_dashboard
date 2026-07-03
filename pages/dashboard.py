"""Dashboard page for the Nebula Creator Dashboard.

Purpose:
- Render the main landing page for creators: metrics, charts, recent
  collaborations, upcoming tasks, notifications and quick actions.

Public API:
- `render_page()` - Streamlit entry point for this page module. The app's
  router will call this when the user navigates to "Dashboard".

Design principles:
- Keep UI and data separate. This page expects a `data.dummy_data` module to
  provide dummy datasets. If that module isn't available yet, the page will
  produce a lightweight fallback dataset so the UI remains demonstrable.
- All visualizations use Plotly express for interactivity and to keep the
  rendering code reusable.

Future improvements:
- Replace the dummy data import with API calls once a backend exists.
- Extract chart builders into `components/charts.py` for reuse across pages.
"""

from __future__ import annotations

from typing import Any, Dict, List

import streamlit as st

try:
    # The project will provide structured dummy data in `data/dummy_data.py`.
    from data.dummy_data import get_dashboard_data  # type: ignore
except Exception:
    get_dashboard_data = None  # will create a fallback later

import pandas as pd
import numpy as np
import plotly.express as px


def _fallback_data() -> Dict[str, Any]:
    """Generate small fallback datasets when `data.dummy_data` isn't present.

    This keeps the UI working while the dedicated dummy data module is being
    added (or when the app is run in a test environment).
    """

    months = pd.date_range(end=pd.Timestamp.today(), periods=12, freq="ME").strftime("%b %Y")
    monthly_earnings = pd.Series(np.linspace(1200, 5200, num=12).round(2), index=months)

    campaign_perf = pd.DataFrame(
        {
            "campaign": [f"Campaign {i+1}" for i in range(6)],
            "clicks": np.random.randint(200, 4500, size=6),
            "conversions": np.random.randint(10, 500, size=6),
            "impressions": np.random.randint(1000, 50000, size=6),
            "status": np.random.choice(["Active", "Paused", "Completed"], size=6),
        }
    )

    engagement = pd.Series(np.clip(np.random.normal(2.5, 0.8, size=12).cumsum() / 12, 0.5, 10).round(2), index=months)

    recent_collabs = [
        {"brand": "Aurora Labs", "project": "Product Photoshoot", "role": "Photographer", "status": "Completed"},
        {"brand": "PulseAI", "project": "Explainer Video", "role": "Editor", "status": "Active"},
        {"brand": "GreenSpark", "project": "Social Reels", "role": "Creator", "status": "Pending"},
    ]

    tasks = [
        {"task": "Edit PulseAI cut", "due": "2026-07-10", "priority": "High", "progress": 40},
        {"task": "Submit Aurora deliverables", "due": "2026-07-18", "priority": "Medium", "progress": 100},
    ]

    notifications = [
        {"text": "Payment of $1,200 completed for Aurora Labs", "type": "payment"},
        {"text": "New campaign: GreenSpark wants creators", "type": "campaign"},
    ]

    metrics = {
        "total_campaigns": 24,
        "active_campaigns": int((campaign_perf["status"] == "Active").sum()),
        "earnings": int(monthly_earnings.sum()),
        "followers": 25300,
        "engagement_rate": "2.8%",
    }

    return {
        "metrics": metrics,
        "monthly_earnings": monthly_earnings,
        "campaign_performance": campaign_perf,
        "engagement_growth": engagement,
        "recent_collaborations": recent_collabs,
        "upcoming_tasks": tasks,
        "notifications": notifications,
    }


def render_metrics(metrics: Dict[str, Any]) -> None:
    """Render top metric cards in a horizontal layout.

    Uses `st.metric` for a simple, accessible metric presentation. For a more
    sophisticated visual style, consider moving this into `components/cards.py`.
    """

    st.subheader("Welcome back, Creator!")
    cols = st.columns(5)
    cols[0].metric("Total Campaigns", metrics.get("total_campaigns", "—"))
    cols[1].metric("Active Campaigns", metrics.get("active_campaigns", "—"))
    cols[2].metric("Earnings", f"${metrics.get('earnings', '—')}")
    cols[3].metric("Followers", f"{metrics.get('followers', '—')}")
    cols[4].metric("Engagement Rate", metrics.get("engagement_rate", "—"))


def render_charts(monthly_earnings: pd.Series, campaign_performance: pd.DataFrame, engagement_growth: pd.Series) -> None:
    """Render the main charts: monthly earnings, campaign performance, engagement.

    Parameters:
    - `monthly_earnings`: indexed series of earnings per month.
    - `campaign_performance`: dataframe with campaign metrics.
    - `engagement_growth`: series with engagement metric over time.
    """

    st.markdown("## Performance")
    c1, c2 = st.columns([2, 1])

    # Monthly earnings line chart
    fig_earn = px.line(x=monthly_earnings.index, y=monthly_earnings.values, labels={"x": "Month", "y": "Earnings ($)"}, title="Monthly Earnings")
    fig_earn.update_traces(line=dict(color="#6366f1", width=3))
    c1.plotly_chart(fig_earn, use_container_width=True)

    # Campaign performance bar chart (top campaigns by conversions)
    top_campaigns = campaign_performance.sort_values("conversions", ascending=False).head(5)
    fig_campaign = px.bar(top_campaigns, x="campaign", y="conversions", title="Top Campaigns by Conversions", labels={"conversions": "Conversions"}, color_discrete_sequence=["#10b981"])
    c2.plotly_chart(fig_campaign, use_container_width=True)

    # Engagement growth below
    st.markdown("### Engagement Growth")
    fig_eng = px.area(x=engagement_growth.index, y=engagement_growth.values, labels={"x": "Month", "y": "Engagement"}, title="Engagement Growth")
    fig_eng.update_traces(fillcolor="#f97316", line=dict(color="#fb923c"))
    st.plotly_chart(fig_eng, use_container_width=True)


def render_recent_collaborations(collabs: List[Dict[str, Any]]) -> None:
    """Show a compact list of recent collaborations with basic details.

    Each item includes brand, project, role, and status. In a production app
    these would be links to a collaboration detail view.
    """

    st.markdown("## Recent Collaborations")
    for c in collabs:
        st.markdown(f"**{c['brand']}**  —  {c['project']}  •  {c['role']}  —  **{c['status']}**")


def render_tasks(tasks: List[Dict[str, Any]]) -> None:
    """Render a minimal tasks view with progress indicators.

    Actions such as marking complete or adding tasks are UI-only for the
    prototype; hook them to backend endpoints once available.
    """

    st.markdown("## Upcoming Tasks")
    for task in tasks:
        st.markdown(f"- {task['task']} — due {task['due']} — {task['priority']}")
        st.progress(task.get("progress", 0))


def render_notifications(notifs: List[Dict[str, Any]]) -> None:
    """Display recent notifications in a small list.

    Notifications are intentionally read-only in the prototype. When a backend
    exists, these can be pulled from a notifications API and support
    mark-as-read mutations.
    """

    st.markdown("## Notifications")
    for n in notifs:
        st.info(n["text"])


def render_quick_actions() -> None:
    """Render quick action buttons in a compact layout.

    Buttons currently navigate client-side via session state. Replace these
    handlers with RPCs or navigation helpers once the app routing evolves.
    """

    st.markdown("## Quick Actions")
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("Apply Campaign"):
        # Update the app's session state so the router navigates to the
        # Campaigns page. Avoid experimental APIs for compatibility.
        st.session_state.active_page = "Campaigns"
    if c2.button("Upload Content"):
        st.session_state.active_page = "Dashboard"
    if c3.button("View Analytics"):
        st.session_state.active_page = "Analytics"
    if c4.button("Edit Profile"):
        st.session_state.active_page = "My Profile"


def render_page() -> None:
    """Streamlit entry point for this page.

    The router in `app.py` imports this module and calls `render_page()` when
    the user navigates to the Dashboard page.
    """

    # Acquire data from the dedicated dummy data module when available. This
    # keeps the page free of hardcoded data and centralizes dummy datasets.
    if get_dashboard_data is not None:
        data = get_dashboard_data()
    else:
        st.warning("`data/dummy_data.py` not found — using fallback demo data.")
        data = _fallback_data()

    metrics = data["metrics"]
    monthly_earnings = data["monthly_earnings"]
    campaign_performance = data["campaign_performance"]
    engagement_growth = data["engagement_growth"]
    recent_collaborations = data["recent_collaborations"]
    upcoming_tasks = data["upcoming_tasks"]
    notifications = data["notifications"]

    # Layout
    render_metrics(metrics)
    render_charts(monthly_earnings, campaign_performance, engagement_growth)

    # Two-column area for collaborations/tasks/notifications
    left, right = st.columns([2, 1])
    with left:
        render_recent_collaborations(recent_collaborations)
    with right:
        render_tasks(upcoming_tasks)
        render_notifications(notifications)

    st.markdown("---")
    render_quick_actions()


if __name__ == "__main__":
    render_page()
