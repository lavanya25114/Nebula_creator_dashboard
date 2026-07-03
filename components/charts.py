"""Reusable chart helpers using Plotly for the Nebula Creator Dashboard.

Purpose:
- Provide thin wrappers around Plotly Express so pages call a consistent
  interface when rendering charts.

Public functions:
- `line_chart(x, y, title, **px_kwargs)`
- `bar_chart(df, x, y, title, **px_kwargs)`
- `area_chart(x, y, title, **px_kwargs)`

Design notes:
- Keep these wrappers minimal; they should not perform heavy data cleaning.
  That responsibility belongs to the page or a data layer.
"""

from __future__ import annotations

from typing import Any, Optional

import plotly.express as px
import streamlit as st


def line_chart(x, y, title: str = "", **px_kwargs: Any) -> None:
    """Render a simple line chart.

    Parameters `x` and `y` are arrays or pandas Series. Additional Plotly
    Express kwargs can be passed via `px_kwargs`.
    """

    fig = px.line(x=x, y=y, title=title, **px_kwargs)
    # Wrap charts in a nebula-card for consistent padding and background.
    st.markdown("<div class='nebula-card'>", unsafe_allow_html=True)
    st.plotly_chart(fig, width='stretch')
    st.markdown("</div>", unsafe_allow_html=True)


def bar_chart(df, x: str, y: str, title: str = "", **px_kwargs: Any) -> None:
    """Render a bar chart from a DataFrame.

    Keeps argument shape similar to `px.bar` but encapsulates `st.plotly_chart`
    for consistent rendering.
    """

    fig = px.bar(df, x=x, y=y, title=title, **px_kwargs)
    st.markdown("<div class='nebula-card'>", unsafe_allow_html=True)
    st.plotly_chart(fig, width='stretch')
    st.markdown("</div>", unsafe_allow_html=True)


def area_chart(x, y, title: str = "", **px_kwargs: Any) -> None:
    """Render an area chart.

    Useful for stacked or single-series cumulative metrics.
    """

    fig = px.area(x=x, y=y, title=title, **px_kwargs)
    st.markdown("<div class='nebula-card'>", unsafe_allow_html=True)
    st.plotly_chart(fig, width='stretch')
    st.markdown("</div>", unsafe_allow_html=True)
