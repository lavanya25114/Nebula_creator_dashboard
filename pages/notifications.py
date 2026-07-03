"""Notifications page for the Nebula Creator Dashboard.

Purpose:
- List recent notifications, allow marking as read, and show notification
  settings. Uses `data.dummy_data.get_notifications()` when available or a
  fallback list.
"""

from __future__ import annotations

from typing import Any, Dict, List

import streamlit as st

try:
    from data.dummy_data import get_notifications  # type: ignore
except Exception:
    get_notifications = None

from datetime import datetime, timedelta


def _fallback_notifications() -> List[Dict[str, Any]]:
    now = datetime.now()
    return [
        {"id": "n1", "text": "Payment of $1,200 completed for Aurora Labs", "type": "payment", "ts": now - timedelta(days=1), "read": False},
        {"id": "n2", "text": "New campaign: GreenSpark wants creators", "type": "campaign", "ts": now - timedelta(days=2), "read": False},
        {"id": "n3", "text": "Your application to NovaWear was accepted", "type": "application", "ts": now - timedelta(days=10), "read": True},
    ]


def render_page() -> None:
    st.title("Notifications")

    if get_notifications is not None:
        notifs = get_notifications()
    else:
        st.info("`data/dummy_data.py` not found — using fallback notifications.")
        notifs = _fallback_notifications()

    unread = [n for n in notifs if not n.get("read")]
    st.subheader(f"Unread ({len(unread)})")
    for n in unread:
        cols = st.columns([8, 1])
        cols[0].info(f"{n['text']} — {n['ts'].strftime('%Y-%m-%d')}")
        if cols[1].button("Mark read", key=f"mr_{n['id']}"):
            st.success("Marked as read (UI-only). Connect to backend to persist state.")

    st.subheader("All Notifications")
    for n in notifs:
        status = "(read)" if n.get("read") else "(unread)"
        st.write(f"- {n['text']} — {n['ts'].strftime('%Y-%m-%d')} {status}")


if __name__ == "__main__":
    render_page()
