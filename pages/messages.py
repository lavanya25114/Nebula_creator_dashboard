"""Messages page for the Nebula Creator Dashboard.

Purpose:
- Provide a simple messaging UI: conversation list, chat window, recent
  messages, unread counts and search. Uses dummy data from
  `data.dummy_data.get_messages()` when available; otherwise provides a
  fallback set.

Public API:
- `render_page()` - Streamlit callable used by the router.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import streamlit as st

try:
    from data.dummy_data import get_messages  # type: ignore
except Exception:
    get_messages = None

from datetime import datetime, timedelta


def _fallback_messages() -> Dict[str, Any]:
    """Return a minimal messages dataset for the prototype.

    Structure:
    - conversations: list of {id, name, unread, last_message, messages}
    - messages: list of {sender, text, ts}
    """

    now = datetime.now()
    convs = [
        {
            "id": "c1",
            "name": "Aurora Labs",
            "unread": 0,
            "last_message": "Thanks — got the final files!",
            "messages": [
                {"sender": "Aurora", "text": "Thanks — got the final files!", "ts": now - timedelta(hours=2)},
                {"sender": "You", "text": "Great — sending invoice.", "ts": now - timedelta(hours=3)},
            ],
        },
        {
            "id": "c2",
            "name": "PulseAI",
            "unread": 2,
            "last_message": "Can you make the edits by tomorrow?",
            "messages": [
                {"sender": "PulseAI", "text": "Can you make the edits by tomorrow?", "ts": now - timedelta(minutes=45)},
                {"sender": "You", "text": "Yes, will do.", "ts": now - timedelta(hours=1)},
            ],
        },
    ]

    return {"conversations": convs}


def _select_conversation(conversations: List[Dict[str, Any]], cid: Optional[str]) -> Dict[str, Any]:
    if cid:
        for c in conversations:
            if c["id"] == cid:
                return c
    # default to first
    return conversations[0]


def render_page() -> None:
    """Render the messages page.

    The page intentionally keeps message persistence out of scope — hooking
    to a real-time or REST messaging backend is a future step.
    """

    st.title("Messages")

    if get_messages is not None:
        data = get_messages()
    else:
        st.info("`data/dummy_data.py` not found — using fallback messages.")
        data = _fallback_messages()

    conversations = data.get("conversations", [])
    search = st.text_input("Search conversations")

    # Left column: list of conversations
    left, right = st.columns([1, 3])
    with left:
        st.subheader("Conversations")
        filtered = [c for c in conversations if search.lower() in c["name"].lower()] if search else conversations
        for c in filtered:
            label = f"{c['name']} ({c.get('unread', 0)})" if c.get("unread", 0) else c['name']
            if st.button(label, key=f"conv_{c['id']}"):
                st.session_state.selected_conv = c['id']

    # Determine selected conversation
    cid = st.session_state.get("selected_conv") if "selected_conv" in st.session_state else (conversations[0]['id'] if conversations else None)
    if conversations:
        conv = _select_conversation(conversations, cid)
    else:
        st.write("No conversations")
        return

    # Right: chat window
    with right:
        st.subheader(conv['name'])
        for m in conv['messages']:
            ts = m['ts'].strftime('%Y-%m-%d %H:%M') if hasattr(m['ts'], 'strftime') else str(m['ts'])
            if m['sender'] == 'You':
                st.markdown(f"<div style='text-align:right'><b>You</b>: {m['text']}<br/><small>{ts}</small></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='text-align:left'><b>{m['sender']}</b>: {m['text']}<br/><small>{ts}</small></div>", unsafe_allow_html=True)

        # Compose area
        st.markdown("---")
        with st.form(key="send_msg"):
            msg = st.text_area("Message", value="")
            submitted = st.form_submit_button("Send")
            if submitted and msg.strip():
                st.success("Message sent (UI-only). Connect to messaging backend to persist and deliver messages.")


if __name__ == "__main__":
    render_page()
