"""Creator Profile page for the Nebula Creator Dashboard.

Purpose:
- Display creator profile information: avatar, bio, social links, skills,
  audience stats, and portfolio. This page is read-first: edits are handled
  by an `Edit Profile` action that will eventually open a form or a modal.

Public API:
- `render_page()` - Streamlit callable used by the app router.

Design notes:
- Data is supplied by `data.dummy_data.get_profile_data()` when available.
- The UI is intentionally static and frontend-oriented so backend
  integration can replace the data provider without changing layout code.
"""

from __future__ import annotations

from typing import Any, Dict, List

import streamlit as st

try:
    from data.dummy_data import get_profile_data  # type: ignore
except Exception:
    get_profile_data = None


def _fallback_profile() -> Dict[str, Any]:
    """Return a small, self-contained profile dict for demo purposes.

    Kept lightweight to avoid hard dependencies when rendering the page in
    isolation.
    """

    return {
        "name": "Ava Rivera",
        "bio": "Visual storyteller — photography & short-form video. Collaborates with startups on product launches and social campaigns.",
        "avatar": None,  # Leave None; UI will use a placeholder.
        "social": {
            "Instagram": "@ava.rivera",
            "YouTube": "Ava Rivera",
            "LinkedIn": "ava-rivera",
            "Twitter": "@avar_creates",
        },
        "skills": ["Photography", "Video Editing", "Social Strategy", "Styling"],
        "categories": ["Product", "Lifestyle", "Tech"],
        "location": "Los Angeles, CA",
        "languages": ["English", "Spanish"],
        "portfolio": [
            {"title": "Aurora Labs Product Shoot", "type": "Photography"},
            {"title": "PulseAI Explainer Cut", "type": "Video Editing"},
        ],
        "followers": 25300,
        "avg_reach": "18k",
        "engagement_rate": "2.8%",
    }


def render_profile_card(profile: Dict[str, Any]) -> None:
    """Render the top profile card with avatar, name and quick stats.

    This function focuses solely on presentation. Mutations (edit/save)
    should be implemented separately so the UI remains declarative.
    """

    cols = st.columns([1, 3])

    # Avatar placeholder (when a proper image URL is available, show it).
    avatar = profile.get("avatar") or "https://via.placeholder.com/120"
    with cols[0]:
        st.image(avatar, width=120)

    with cols[1]:
        st.header(profile.get("name", "Creator"))
        st.write(profile.get("bio", ""))
        st.write("\n")
        st.markdown(f"**Followers:** {profile.get('followers', '—')}  •  **Avg Reach:** {profile.get('avg_reach', '—')}  •  **Engagement:** {profile.get('engagement_rate', '—')}")


def render_profile_details(profile: Dict[str, Any]) -> None:
    """Render additional profile sections: social links, skills, portfolio.

    Each section is intentionally simple and readable; move these into
    `components/cards.py` when the design needs to be shared with other
    pages.
    """

    st.subheader("Social Links")
    social = profile.get("social", {})
    for name, handle in social.items():
        st.markdown(f"- **{name}**: {handle}")

    st.subheader("Skills & Categories")
    st.markdown(f"**Skills:** {', '.join(profile.get('skills', []))}")
    st.markdown(f"**Categories:** {', '.join(profile.get('categories', []))}")

    st.subheader("Portfolio")
    for item in profile.get("portfolio", []):
        st.markdown(f"- {item['title']} — *{item['type']}*")


def render_page() -> None:
    """Streamlit page entrypoint used by the router.

    This function isolates rendering concerns from data acquisition so the
    same UI can be used with dummy data, a local file, or a remote API.
    """

    if get_profile_data is not None:
        profile = get_profile_data()
    else:
        st.info("`data/dummy_data.py` not found — using fallback profile.")
        profile = _fallback_profile()

    render_profile_card(profile)
    st.markdown("---")
    render_profile_details(profile)

    st.markdown("---")
    if st.button("Edit Profile"):
        st.success("Edit flow placeholder — replace with a modal or form connected to backend APIs.")


if __name__ == "__main__":
    render_page()
