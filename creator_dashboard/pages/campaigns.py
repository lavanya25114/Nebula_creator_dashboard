"""Campaigns page for the Nebula Creator Dashboard.

Purpose:
- List available campaigns, support searching, filtering and sorting, and
  provide an `Apply` action. The page uses dummy data from
  `data.dummy_data.get_campaigns()` when available, otherwise generates a
  lightweight fallback dataset.

Public API:
- `render_page()` - Streamlit entry point for this page module.

Design notes:
- UI is read-first and stateless: applying to a campaign currently shows a
  confirmation message. When a backend exists this should call an API.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import streamlit as st

try:
    from data.dummy_data import get_campaigns  # type: ignore
except Exception:
    get_campaigns = None

import pandas as pd
import datetime as dt


def _fallback_campaigns() -> List[Dict[str, Any]]:
    """Return a list of demo campaign dicts for the UI prototype.

    Each campaign includes: brand, name, description, budget, deadline, and
    status. Keep data minimal and replaceable by the `data` module later.
    """

    today = dt.date.today()
    items = [
        {
            "brand": "Aurora Labs",
            "name": "Aurora Launch Shoot",
            "description": "Product photoshoot and short-form video for the Aurora launch.",
            "budget": 3500,
            "deadline": today + dt.timedelta(days=21),
            "status": "Open",
        },
        {
            "brand": "GreenSpark",
            "name": "GreenSpark Reels Campaign",
            "description": "Create 6 short reels showcasing eco-friendly features.",
            "budget": 1800,
            "deadline": today + dt.timedelta(days=10),
            "status": "Open",
        },
        {
            "brand": "PulseAI",
            "name": "Explainer Video Edit",
            "description": "Edit a 90s explainer video and two social cuts.",
            "budget": 2200,
            "deadline": today + dt.timedelta(days=5),
            "status": "Closed",
        },
        {
            "brand": "NovaWear",
            "name": "Lifestyle Photoshoot",
            "description": "Outdoor lifestyle photography and social assets.",
            "budget": 4200,
            "deadline": today + dt.timedelta(days=40),
            "status": "Open",
        },
    ]
    return items


def _filter_and_sort(campaigns: List[Dict[str, Any]], query: str, status: Optional[str], sort_by: str) -> List[Dict[str, Any]]:
    """Filter and sort campaigns according to UI controls.

    Parameters
    - campaigns: list of campaign dicts
    - query: search string applied to brand/name/description
    - status: status filter (e.g., Open/Closed/All)
    - sort_by: 'Deadline' | 'Budget (high->low)' | 'Budget (low->high)'
    """

    df = pd.DataFrame(campaigns)
    if query:
        q = query.lower()
        df = df[df.apply(lambda r: q in str(r["brand"]).lower() or q in str(r["name"]).lower() or q in str(r["description"]).lower(), axis=1)]

    if status and status != "All":
        df = df[df["status"] == status]

    if sort_by == "Deadline":
        df = df.sort_values(by="deadline")
    elif sort_by == "Budget (high->low)":
        df = df.sort_values(by="budget", ascending=False)
    else:
        df = df.sort_values(by="budget", ascending=True)

    # Convert datetimes to date for display
    df["deadline"] = pd.to_datetime(df["deadline"]).dt.date

    return df.to_dict(orient="records")


def _render_campaign_card(c: Dict[str, Any]) -> None:
    """Render a single campaign card using Streamlit's simple primitives.

    Keep the card minimal and consistent with the app design; integrate a
    modal or separate page for a detailed campaign view in the future.
    """

    st.markdown(f"**{c['brand']}** — {c['name']}")
    st.write(c["description"])
    cols = st.columns([1, 1, 1])
    cols[0].markdown(f"**Budget**\n${c['budget']}")
    cols[1].markdown(f"**Deadline**\n{c['deadline']}")
    cols[2].markdown(f"**Status**\n{c['status']}")

    if st.button("Apply", key=f"apply_{c['brand']}_{c['name']}"):
        st.success(f"Applied to {c['name']} — the application flow will be connected to the backend later.")


def render_page() -> None:
    """Streamlit entrypoint for the Campaigns page.

    Renders a search bar, filters, and campaign cards. Data is provided by
    `data.dummy_data.get_campaigns()` when available; otherwise fallback data
    is used.
    """

    st.title("Campaigns")

    if get_campaigns is not None:
        campaigns = get_campaigns()
    else:
        st.info("`data/dummy_data.py` not found — using fallback campaign data.")
        campaigns = _fallback_campaigns()

    # Controls: search, status filter, sorting
    with st.form(key="campaign_controls"):
        qcol1, qcol2, qcol3 = st.columns([3, 1, 1])
        query = qcol1.text_input("Search campaigns", value="")
        status = qcol2.selectbox("Status", ["All", "Open", "Closed"], index=0)
        sort_by = qcol3.selectbox("Sort by", ["Deadline", "Budget (high->low)", "Budget (low->high)"])
        submitted = st.form_submit_button("Apply")

    # Apply filters even if the form was not submitted to keep experience snappy
    filtered = _filter_and_sort(campaigns, query, status, sort_by)

    st.markdown(f"### {len(filtered)} campaigns")

    for c in filtered:
        st.container()
        _render_campaign_card(c)
        st.markdown("---")


if __name__ == "__main__":
    render_page()
