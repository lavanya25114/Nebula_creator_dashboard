"""Reusable table helpers for the Nebula Creator Dashboard.

Purpose:
- Provide a small abstraction for rendering pandas DataFrames with consistent
  formatting and optional download/export helpers.

Public functions:
- `render_dataframe(df, formats=None)` - render df with optional formatting.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

import streamlit as st


def render_dataframe(df, formats: Optional[Dict[str, str]] = None) -> None:
    """Render a DataFrame with simple formatting applied.

    Parameters:
    - `df`: pandas DataFrame
    - `formats`: optional dict mapping column -> format string for styling
    """

    # Wrap the table in the shared card style for consistent spacing and
    # background. Use Streamlit's modern `width` argument for layout.
    st.markdown("<div class='nebula-card'>", unsafe_allow_html=True)
    if formats:
        try:
            st.dataframe(df.style.format(formats), width='stretch')
            st.markdown("</div>", unsafe_allow_html=True)
            return
        except Exception:
            st.dataframe(df, width='stretch')
            st.markdown("</div>", unsafe_allow_html=True)
            return

    st.dataframe(df, width='stretch')
    st.markdown("</div>", unsafe_allow_html=True)
