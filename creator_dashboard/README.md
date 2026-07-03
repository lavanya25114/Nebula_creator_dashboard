# Nebula Creator Dashboard (Prototype)

This repository contains a Streamlit-based prototype of the Nebula Accelerator
Creator Dashboard. The UI is modular, component-driven, and data-agnostic —
dummy data lives inside `data/dummy_data.py` and pages are located under
`pages/`.

Quick start

1. Create and activate a Python virtual environment (macOS / Linux):

```bash
cd creator_dashboard
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501` by default.

Project structure

- `app.py` - Streamlit entrypoint and router
- `pages/` - Page modules (dashboard, profile, campaigns, analytics, etc.)
- `components/` - Reusable UI components (cards, charts, tables, sidebar)
- `data/dummy_data.py` - Centralized dummy data providers

Future work

- Replace dummy data providers with API clients
- Add authentication and backend integration
- Extract shared layout and style tokens into a single theme module
