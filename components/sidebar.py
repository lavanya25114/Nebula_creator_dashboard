"""Sidebar component for the Nebula Creator Dashboard.

Purpose:
- Provide a reusable, centralized sidebar renderer used by `app.py`.
- Keep navigation state consistent across Streamlit reruns.

Public API:
- `render_sidebar(current_page: str, page_order: list[str]) -> str`
  Renders the sidebar and returns the newly selected page (or the same page
  if nothing changed).

Design notes / future improvements:
- Uses simple unicode icons to avoid external asset dependencies.
- When a backend exists, navigation items and quick-actions can be fetched
  from an API to enable role-based access and feature toggles.
"""

from __future__ import annotations

from typing import Iterable

import streamlit as st

# Navigation items shown in the sidebar in the default order.
NAV_ITEMS = [
    ("🏠", "Dashboard"),
    ("👤", "My Profile"),
    ("🚀", "Campaigns"),
    ("🤝", "Collaborations"),
    ("📊", "Analytics"),
    ("💰", "Earnings"),
    ("✅", "Tasks"),
    ("💬", "Messages"),
    ("🔔", "Notifications"),
    ("⚙", "Settings"),
]


def _format_label(icon: str, label: str) -> str:
    """Return a compact label combining an icon and a text label.

    This helper centralizes formatting so the visual contract is consistent
    across the sidebar and easier to update (e.g., to swap icons later).
    """

    return f"{icon}  {label}"


def render_sidebar(current_page: str, page_order: Iterable[str]) -> str:
    """Render the application sidebar and return the selected page.

    Parameters
    - current_page: the page currently stored in session state (keeps radio
      selection stable across reruns).
    - page_order: ordered list of page display names (used to preserve any
      custom ordering from the app shell).

    Returns
    - The name of the selected page. The caller usually stores this into
      `st.session_state.active_page`.

    Notes
    - Keep this function pure from business logic: it only renders UI and
      returns a selection. Data fetching and page rendering are the
      responsibility of page modules.
    - This file intentionally avoids side effects other than rendering UI so
      it is safe to import during unit tests.
    """

    st.sidebar.title("Nebula Creator")
    st.sidebar.caption("Creator workspace for the Nebula Accelerator Platform")

    # Search - keeps the UI responsive even without a backend. In the future
    # this can be wired to a search API to filter campaigns, messages, etc.
    with st.sidebar.form(key="sidebar_search", clear_on_submit=False):
        search_query = st.text_input("Search", value="", placeholder="Search campaigns, messages...")
        st.form_submit_button("Go")

    st.sidebar.markdown("---")

    # Build radio options based on page_order so the app-level ordering wins
    # when the developer wants to change page arrangement from `app.py`.
    labels = []
    label_to_name = {}
    for name in page_order:
      # find matching icon for each page name, default to a dot if missing
      icon = next((ic for ic, nm in NAV_ITEMS if nm == name), "•")
      label = _format_label(icon, name)
      labels.append(label)
      label_to_name[label] = name

    # Compute the index of current page in the labels list, default to 0
    try:
      current_icon = next(ic for ic, nm in NAV_ITEMS if nm == current_page)
      index = labels.index(_format_label(current_icon, current_page))
    except Exception:
      index = 0

    # Render navigation. Use a mapping to reliably convert the displayed
    # label back to the canonical page name instead of string-splitting.
    selected = st.sidebar.radio("Navigate", labels, index=index)
    selected_page = label_to_name.get(selected, selected)

    st.sidebar.markdown("---")

    # Quick actions are simple buttons for common creator flows. These should
    # only trigger navigation or emit events; heavy logic or mutations belong
    # in the page modules or backend services.
    st.sidebar.subheader("Quick Actions")
    if st.sidebar.button("Apply Campaign"):
        return "Campaigns"
    if st.sidebar.button("Upload Content"):
        return "Dashboard"
    if st.sidebar.button("View Analytics"):
        return "Analytics"
    if st.sidebar.button("Edit Profile"):
        return "My Profile"

    # Compact profile preview at the bottom of sidebar — use nebula-card for
    # consistent spacing and background.
    st.sidebar.markdown("\n---\n")
    st.sidebar.markdown("<div class='nebula-card'>", unsafe_allow_html=True)
    st.sidebar.caption("Signed in as")
    st.sidebar.markdown("**Creator Name**\n\nPhotographer • 25.3k followers")
    st.sidebar.markdown("</div>", unsafe_allow_html=True)

    return selected_page
