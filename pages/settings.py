"""Settings page for the Nebula Creator Dashboard.

Purpose:
- Allow creators to update profile/account settings, notification preferences,
  privacy and theme choices. This UI is a prototype; form submissions are
  currently UI-only and should be wired to backend APIs in the future.
"""

from __future__ import annotations

from typing import Any, Dict

import streamlit as st


def render_profile_settings() -> None:
    st.subheader("Profile Settings")
    name = st.text_input("Display name", value="Ava Rivera")
    bio = st.text_area("Bio", value="Visual storyteller — photography & short-form video.")
    if st.button("Save Profile"):
        st.success("Profile settings saved (UI-only). Hook up backend APIs to persist changes.")


def render_account_settings() -> None:
    st.subheader("Account Settings")
    email = st.text_input("Email", value="ava@example.com")
    if st.button("Save Account"):
        st.success("Account settings saved (UI-only).")


def render_notification_preferences() -> None:
    st.subheader("Notification Preferences")
    email_n = st.checkbox("Email notifications", value=True)
    sms_n = st.checkbox("SMS notifications", value=False)
    if st.button("Save Notifications"):
        st.success("Notification preferences saved (UI-only).")


def render_privacy_settings() -> None:
    st.subheader("Privacy")
    st.radio("Profile visibility", ["Public", "Private"], index=0)
    if st.button("Save Privacy"):
        st.success("Privacy settings saved (UI-only).")


def render_theme_settings() -> None:
    st.subheader("Theme")
    theme = st.selectbox("Theme", ["Light", "Dark"], index=0)
    if st.button("Apply Theme"):
        st.success("Theme applied (UI-only). Use CSS or native Streamlit theming for persistence.")


def render_page() -> None:
    st.title("Settings")
    render_profile_settings()
    st.markdown("---")
    render_account_settings()
    st.markdown("---")
    render_notification_preferences()
    st.markdown("---")
    render_privacy_settings()
    st.markdown("---")
    render_theme_settings()
    st.markdown("---")
    if st.button("Logout"):
        st.warning("Logout placeholder. Integrate with auth service to end session.")


if __name__ == "__main__":
    render_page()
