"""Theme helper for the Nebula Creator Dashboard.

Purpose:
- Centralize simple design tokens and a small CSS injection helper so the
  app's visual language is consistent across components.

Public API:
- `apply_theme()` - inject CSS + set lightweight design variables.

Design notes:
- Keep this file minimal. For a more advanced design system consider
  extracting tokens to JSON and generating CSS variables consumed by the UI.
"""

from __future__ import annotations

import streamlit as st

# Color tokens used across components. Keep names semantic to make future
# branding changes straightforward.
PALETTE = {
    "bg": "#f8fafc",
    "card_bg": "#ffffff",
    "muted": "#6b7280",
    "border": "#e6e9ef",
    "primary": "#6366f1",
    "accent": "#10b981",
}


def apply_theme() -> None:
    """Inject minimal shared CSS to keep spacing, cards and typography consistent.

    This function is safe to call on every rerun; Streamlit ignores duplicate
    style tags so idempotence is preserved.
    """

    css = f"""
    <style>
      .stApp {{ background: {PALETTE['bg']}; color: #0f172a; }}
      .block-container {{ padding-top: 1.5rem; padding-bottom: 2rem; }}
      .nebula-card {{ background: {PALETTE['card_bg']}; border: 1px solid {PALETTE['border']}; border-radius: 10px; padding: 12px; box-shadow: 0 1px 2px rgba(15,23,42,0.04); }}
      .nebula-muted {{ color: {PALETTE['muted']}; }}
      .nebula-primary {{ color: {PALETTE['primary']}; }}
      .nebula-accent {{ color: {PALETTE['accent']}; }}
      .nebula-metric {{ font-size: 20px; font-weight:600; }}
    </style>
    """

    st.markdown(css, unsafe_allow_html=True)
