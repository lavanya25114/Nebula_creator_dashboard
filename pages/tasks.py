"""Tasks page for the Nebula Creator Dashboard.

Purpose:
- Provide a simple task manager for creators: list tasks, add new tasks,
  mark complete, and show progress. This is UI-first and uses dummy data or
  a fallback.

Public API:
- `render_page()` - Streamlit callable for the tasks page.
"""

from __future__ import annotations

from typing import Any, Dict, List

import streamlit as st

try:
    from data.dummy_data import get_tasks  # type: ignore
except Exception:
    get_tasks = None

import pandas as pd
from datetime import date, timedelta


def _fallback_tasks() -> List[Dict[str, Any]]:
    today = date.today()
    return [
        {"name": "Edit PulseAI cut", "due": today + timedelta(days=3), "priority": "High", "progress": 40, "completed": False},
        {"name": "Submit Aurora deliverables", "due": today + timedelta(days=15), "priority": "Medium", "progress": 100, "completed": True},
        {"name": "Prepare GreenSpark storyboard", "due": today + timedelta(days=7), "priority": "High", "progress": 10, "completed": False},
    ]


def render_task_list(tasks: List[Dict[str, Any]]) -> None:
    st.subheader("Tasks")
    for idx, t in enumerate(tasks):
        cols = st.columns([4, 1, 1, 1])
        cols[0].markdown(f"**{t['name']}**\nDue: {t['due']} — {t['priority']}")
        cols[1].progress(t.get("progress", 0))
        if cols[2].button("Complete", key=f"complete_{idx}") and not t.get("completed", False):
            st.success(f"Marked '{t['name']}' as complete (UI-only). Connect to backend to persist changes.")
        if cols[3].button("Edit", key=f"edit_{idx}"):
            st.info("Edit flow placeholder — implement modal or separate form to edit tasks.")
        st.markdown("---")


def render_add_task_form() -> None:
    st.subheader("Add Task")
    with st.form(key="add_task"):
        name = st.text_input("Task name")
        due = st.date_input("Due date")
        priority = st.selectbox("Priority", ["Low", "Medium", "High"], index=1)
        submitted = st.form_submit_button("Add Task")
        if submitted:
            st.success(f"Task '{name}' added (UI-only). Hook up backend to persist tasks.")


def render_page() -> None:
    st.title("Tasks")
    if get_tasks is not None:
        tasks = get_tasks()
    else:
        st.info("`data/dummy_data.py` not found — using fallback tasks.")
        tasks = _fallback_tasks()

    render_add_task_form()
    st.markdown("---")
    render_task_list(tasks)


if __name__ == "__main__":
    render_page()
