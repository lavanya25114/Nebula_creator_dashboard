"""Reusable card components for the Nebula Creator Dashboard.

Purpose:
- Provide small, composable card renderers used across pages. Keeps visual
  patterns consistent and centralizes simple layout rules.

Public functions:
- `render_card(title, body, footer=None, width='100%')` - lightweight card
  with header, body text and optional footer.
- `render_metric_card(label, value, delta=None)` - compact stat card used
  for high-level KPIs.

Design notes:
- Keep functions UI-only. Data retrieval and formatting happen elsewhere.
"""

from __future__ import annotations

from typing import Optional

import streamlit as st


def render_card(title: str, body: str, footer: Optional[str] = None, width: str = "100%") -> None:
    """Render a simple card with title, body and optional footer.

    Parameters:
    - `title`: card title displayed at the top.
    - `body`: main text or markdown content.
    - `footer`: optional small footer text.
    - `width`: CSS-friendly width value; Streamlit controls layout so this
      acts as a hint only.
    """

    # Use the centralized `.nebula-card` class provided by the theme helper
    # so visual updates are driven from a single source of truth.
    st.markdown(f"<div class='nebula-card' style='width:{width}'>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='margin:0 0 8px 0'>{title}</h4>", unsafe_allow_html=True)
    st.markdown(body)
    if footer:
      st.markdown(f"<div class='nebula-muted' style='margin-top:8px;font-size:12px'>{footer}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def render_metric_card(label: str, value: str, delta: Optional[str] = None) -> None:
    """Render a compact metric card.

    This complements `st.metric` when a static HTML-driven style is desired.
    Use `st.metric` for built-in delta animations and accessibility.
    """

    html = f"<div class='nebula-card'><div class='nebula-muted' style='font-size:12px'>{label}</div><div class='nebula-metric' style='margin-top:4px'>{value}</div>"
    if delta:
      html += f"<div class='nebula-accent' style='font-size:12px;margin-top:6px'>{delta}</div>"
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)
