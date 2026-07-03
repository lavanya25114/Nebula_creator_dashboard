"""Collaborations page for the Nebula Creator Dashboard.

Purpose:
- Show current, completed, and pending collaborations. Provide lightweight
  timeline and progress views. This module is UI-only and uses dummy data
  from `data.dummy_data.get_collaborations()` when available.

Public API:
- `render_page()` - Streamlit entrypoint for the Collaborations page.

Notes:
- Keep state mutations (accept/decline, progress updates) in the backend;
  the prototype shows confirmation messages instead of performing permanent
  state changes.
"""

from __future__ import annotations

from typing import Any, Dict, List

import streamlit as st

try:
    from data.dummy_data import get_collaborations  # type: ignore
except Exception:
    get_collaborations = None

import datetime as dt


def _fallback_collabs() -> List[Dict[str, Any]]:
    """Return a small list of collaboration examples for the prototype.

    Each collaboration includes: brand, title, start/end dates, role, status,
    and a numeric progress percentage.
    """

    today = dt.date.today()
    return [
        {
            "brand": "Aurora Labs",
            "title": "Aurora Product Photoshoot",
            "start": today - dt.timedelta(days=45),
            "end": today - dt.timedelta(days=15),
            "role": "Photographer",
            "status": "Completed",
            "progress": 100,
            "details": "Shot product stills and lifestyle images for launch campaign.",
        },
        {
            "brand": "PulseAI",
            "title": "Explainer Video Edit",
            "start": today - dt.timedelta(days=12),
            "end": today + dt.timedelta(days=6),
            "role": "Editor",
            "status": "Active",
            "progress": 60,
            "details": "Editing main explainer + social cuts.",
        },
        {
            "brand": "GreenSpark",
            "title": "Social Reels Series",
            "start": today + dt.timedelta(days=3),
            "end": today + dt.timedelta(days=24),
            "role": "Creator",
            "status": "Pending",
            "progress": 0,
            "details": "Proposal submitted — awaiting brand confirmation.",
        },
    ]


def _render_collab_item(c: Dict[str, Any]) -> None:
    """Render a compact collaboration card with timeline and progress.

    This presentation is focused on clarity and can later be converted to a
    richer component with links to detail pages.
    """

    st.markdown(f"**{c['brand']} — {c['title']}**")
    st.write(c.get("details", ""))
    st.write(f"Role: {c.get('role', '—')}")
    st.write(f"Status: **{c.get('status', '—')}** | {c.get('start')} → {c.get('end')}")
    st.progress(c.get("progress", 0))


def render_page() -> None:
    """Streamlit entrypoint for the Collaborations page.

    The page lists collaborations grouped by status and shows a compact
    timeline. Interactions are placeholders for integration with backend
    workflows later.
    """

    st.title("Collaborations")

    if get_collaborations is not None:
        collabs = get_collaborations()
    else:
        st.info("`data/dummy_data.py` not found — using fallback collaborations.")
        collabs = _fallback_collabs()

    # Group collaborations by status for easy scanning
    groups = {"Active": [], "Completed": [], "Pending": []}
    for c in collabs:
        status = c.get("status", "Pending")
        if status not in groups:
            groups[status] = []
        groups[status].append(c)

    st.subheader("Current Collaborations")
    for c in groups.get("Active", []):
        _render_collab_item(c)
        st.markdown("---")

    st.subheader("Completed Collaborations")
    for c in groups.get("Completed", []):
        _render_collab_item(c)
        st.markdown("---")

    st.subheader("Pending Requests")
    for c in groups.get("Pending", []):
        _render_collab_item(c)
        cols = st.columns(2)
        if cols[0].button("Accept", key=f"accept_{c['brand']}_{c['title']}"):
            st.success(f"Accepted collaboration with {c['brand']}. Connect to backend to persist this change.")
        if cols[1].button("Decline", key=f"decline_{c['brand']}_{c['title']}"):
            st.warning(f"Declined collaboration request from {c['brand']}. Connect to backend to persist this change.")
        st.markdown("---")

    st.sidebar.header("Collaboration Filters")
    timeframe = st.sidebar.selectbox("Timeframe", ["All", "Past 30 days", "Next 30 days"])
    # The timeframe control is a UI placeholder; hooking it to filter logic is
    # a straightforward enhancement when required.


if __name__ == "__main__":
    render_page()
