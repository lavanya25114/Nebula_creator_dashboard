"""Creator Dashboard entry point for the Nebula Accelerator Platform.

This file exists to bootstrap the Streamlit application, define shared page
configuration, and route the user to the correct page module when the rest of
the dashboard is added.

Expected inputs:
- No direct function inputs. Streamlit handles the web session state.

Expected outputs:
- A running Streamlit app shell with navigation and a central content area.

Future improvements:
- Replace the local fallback router with fully dedicated page modules.
- Connect the page router to API-backed data instead of dummy data.
- Add authentication and role-based access control once backend services exist.
"""

from __future__ import annotations

import importlib
from typing import Callable, Optional

import streamlit as st

PAGE_ORDER = [
    "Dashboard",
    "My Profile",
    "Campaigns",
    "Collaborations",
    "Analytics",
    "Earnings",
    "Tasks",
    "Messages",
    "Notifications",
    "Settings",
]

PAGE_MODULES = {
    "Dashboard": "pages.dashboard",
    "My Profile": "pages.profile",
    "Campaigns": "pages.campaigns",
    "Collaborations": "pages.collaborations",
    "Analytics": "pages.analytics",
    "Earnings": "pages.earnings",
    "Tasks": "pages.tasks",
    "Messages": "pages.messages",
    "Notifications": "pages.notifications",
    "Settings": "pages.settings",
}


def configure_page() -> None:
    """Set the Streamlit page metadata and shared app identity.

    This function centralizes the page configuration so all future pages can
    keep the same visual identity without duplicating setup code.
    """

    st.set_page_config(
        page_title="Nebula Creator Dashboard",
        page_icon="✨",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def apply_global_styles() -> None:
    """Inject a small, consistent design system for the dashboard shell.

    The app will later move more styling into reusable component helpers, but
    keeping a tiny shared foundation here makes the initial shell look polished
    and makes future backend integration easier because the layout contract is
    already stable.
    """

    # Keep a small set of global styles, but prefer the centralized theme
    # helper when available. The helper provides a consistent foundation for
    # colors, spacing and card styling.
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {
                background: #ffffff;
                border-right: 1px solid #e5e7eb;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _apply_optional_theme() -> None:
    """Try to apply the shared theme if the component exists.

    We call this at startup so other components can rely on CSS classes like
    `.nebula-card` being available.
    """

    try:
        from components.theme import apply_theme  # type: ignore

        apply_theme()
    except Exception:
        # Theme isn't required; continue with the baseline styles.
        return


def load_renderer(module_path: str, attribute_name: str) -> Optional[Callable[..., None]]:
    """Load a page or component renderer if the module already exists.

    Parameters:
    - module_path: Python import path for the target module.
    - attribute_name: Callable name expected on that module.

    Returns:
    - A callable renderer when the module is available.
    - None when the module does not exist yet or does not expose the attribute.
    """

    try:
        module = importlib.import_module(module_path)
    except ModuleNotFoundError:
        return None

    renderer = getattr(module, attribute_name, None)
    return renderer if callable(renderer) else None


def render_fallback_sidebar(current_page: str) -> str:
    """Render a safe sidebar placeholder until the dedicated sidebar file exists.

    This keeps the app usable while the project is being built one file at a
    time, and it establishes the navigation contract that the later sidebar
    component will implement.
    """

    st.sidebar.title("Nebula Creator")
    st.sidebar.caption("Creator workspace for the Nebula Accelerator Platform")
    selected_page = st.sidebar.radio("Navigate", PAGE_ORDER, index=PAGE_ORDER.index(current_page))
    return selected_page


def render_fallback_content(active_page: str) -> None:
    """Show a temporary content placeholder when a page module is not ready.

    Once the page modules are created, the router will call the dedicated render
    function instead of this placeholder.
    """

    st.title(active_page)
    st.info(
        "This page shell is ready. The dedicated page module will be added next, "
        "followed by reusable sidebar and dashboard components."
    )


def resolve_active_page() -> str:
    """Resolve the current page from session state, keeping navigation stable.

    Streamlit reruns the script on every interaction, so session state is the
    simplest way to preserve the user's current location.
    """

    if "active_page" not in st.session_state:
        st.session_state.active_page = "Dashboard"
    # If the app was navigated using Streamlit's own widgets (for example the
    # radiogroup or generated page links), those widgets may have injected a
    # different value into `st.session_state`. To be resilient we scan the
    # session state for any string that contains a known page name and prefer
    # that when appropriate. This allows both our custom sidebar and the
    # Streamlit-generated navigation to work interchangeably.
    for key, val in st.session_state.items():
        if isinstance(val, str):
            for page in PAGE_ORDER:
                if page.lower() in val.lower():
                    st.session_state.active_page = page
                    return st.session_state.active_page

    return st.session_state.active_page


def route_page(active_page: str) -> None:
    """Render the selected page using a real module or a temporary fallback.

    The later page files will expose simple render functions. This router keeps
    the app structure clean by separating navigation from page content.
    """

    module_path = PAGE_MODULES.get(active_page)
    renderer = load_renderer(module_path, "render_page") if module_path else None

    if renderer is None and active_page == "Dashboard":
        renderer = load_renderer(module_path, "render_dashboard") if module_path else None

    if renderer is not None:
        renderer()
    else:
        render_fallback_content(active_page)


def main() -> None:
    """Run the dashboard shell.

    This function exists so the file remains import-safe for future tests and so
    the application startup path is easy to reuse from any future launcher.
    """

    configure_page()
    apply_global_styles()
    _apply_optional_theme()

    current_page = resolve_active_page()

    sidebar_renderer = load_renderer("components.sidebar", "render_sidebar")
    if sidebar_renderer is not None:
        selected_page = sidebar_renderer(current_page=current_page, page_order=PAGE_ORDER)
        if selected_page:
            st.session_state.active_page = selected_page
    else:
        st.session_state.active_page = render_fallback_sidebar(current_page)

    route_page(st.session_state.active_page)


if __name__ == "__main__":
    main()
