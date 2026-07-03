"""Centralized dummy data providers for the Nebula Creator Dashboard.

Purpose:
- Provide consistent dummy datasets for all pages so UI code remains data-
  agnostic. All pages import the small provider functions below instead of
  hardcoding data.

Design:
- Each function returns small, well-structured Python objects (dicts,
  lists, pandas Series/DataFrames) that match what the page modules expect.
- The module uses a fixed random seed to make demo data deterministic which
  is useful for UI development and screenshots.

Future improvements:
- Replace these providers with API clients that fetch real data from the
  backend. Keep the function signatures stable to minimize changes in the UI.
"""

from __future__ import annotations

from typing import Any, Dict, List

import pandas as pd
import numpy as np
from datetime import date, timedelta


np.random.seed(42)


def get_dashboard_data() -> Dict[str, Any]:
    """Return a dict with the datasets used by `pages.dashboard`.

    Keys:
    - metrics
    - monthly_earnings (pd.Series)
    - campaign_performance (pd.DataFrame)
    - engagement_growth (pd.Series)
    - recent_collaborations (list[dict])
    - upcoming_tasks (list[dict])
    - notifications (list[dict])
    """

    months = pd.date_range(end=pd.Timestamp.today(), periods=12, freq="ME").strftime("%b %Y")
    monthly_earnings = pd.Series(np.linspace(1200, 5200, num=12).round(2), index=months)

    campaign_perf = pd.DataFrame(
        {
            "campaign": [f"Campaign {i+1}" for i in range(6)],
            "clicks": np.random.randint(200, 4500, size=6),
            "conversions": np.random.randint(10, 500, size=6),
            "impressions": np.random.randint(1000, 50000, size=6),
            "status": np.random.choice(["Active", "Paused", "Completed"], size=6),
        }
    )

    engagement = pd.Series(np.clip(np.random.normal(2.5, 0.8, size=12).cumsum() / 12, 0.5, 10).round(2), index=months)

    recent_collabs = [
        {"brand": "Aurora Labs", "project": "Product Photoshoot", "role": "Photographer", "status": "Completed"},
        {"brand": "PulseAI", "project": "Explainer Video", "role": "Editor", "status": "Active"},
        {"brand": "GreenSpark", "project": "Social Reels", "role": "Creator", "status": "Pending"},
    ]

    tasks = [
        {"task": "Edit PulseAI cut", "due": (date.today() + timedelta(days=3)).isoformat(), "priority": "High", "progress": 40},
        {"task": "Submit Aurora deliverables", "due": (date.today() + timedelta(days=15)).isoformat(), "priority": "Medium", "progress": 100},
    ]

    notifications = [
        {"text": "Payment of $1,200 completed for Aurora Labs", "type": "payment"},
        {"text": "New campaign: GreenSpark wants creators", "type": "campaign"},
    ]

    metrics = {
        "total_campaigns": 24,
        "active_campaigns": int((campaign_perf["status"] == "Active").sum()),
        "earnings": int(monthly_earnings.sum()),
        "followers": 25300,
        "engagement_rate": "2.8%",
    }

    return {
        "metrics": metrics,
        "monthly_earnings": monthly_earnings,
        "campaign_performance": campaign_perf,
        "engagement_growth": engagement,
        "recent_collaborations": recent_collabs,
        "upcoming_tasks": tasks,
        "notifications": notifications,
    }


def get_profile_data() -> Dict[str, Any]:
    """Return a profile dictionary consumed by `pages.profile`."""

    return {
        "name": "Ava Rivera",
        "bio": "Visual storyteller — photography & short-form video. Collaborates with startups on product launches and social campaigns.",
        "avatar": None,
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


def get_campaigns() -> List[Dict[str, Any]]:
    """Return a list of campaigns used by `pages.campaigns`."""

    today = date.today()
    return [
        {
            "brand": "Aurora Labs",
            "name": "Aurora Launch Shoot",
            "description": "Product photoshoot and short-form video for the Aurora launch.",
            "budget": 3500,
            "deadline": today + timedelta(days=21),
            "status": "Open",
        },
        {
            "brand": "GreenSpark",
            "name": "GreenSpark Reels Campaign",
            "description": "Create 6 short reels showcasing eco-friendly features.",
            "budget": 1800,
            "deadline": today + timedelta(days=10),
            "status": "Open",
        },
        {
            "brand": "PulseAI",
            "name": "Explainer Video Edit",
            "description": "Edit a 90s explainer video and two social cuts.",
            "budget": 2200,
            "deadline": today + timedelta(days=5),
            "status": "Closed",
        },
        {
            "brand": "NovaWear",
            "name": "Lifestyle Photoshoot",
            "description": "Outdoor lifestyle photography and social assets.",
            "budget": 4200,
            "deadline": today + timedelta(days=40),
            "status": "Open",
        },
    ]


def get_collaborations() -> List[Dict[str, Any]]:
    """Return a list of collaboration examples for `pages.collaborations`."""

    today = date.today()
    return [
        {
            "brand": "Aurora Labs",
            "title": "Aurora Product Photoshoot",
            "start": today - timedelta(days=45),
            "end": today - timedelta(days=15),
            "role": "Photographer",
            "status": "Completed",
            "progress": 100,
            "details": "Shot product stills and lifestyle images for launch campaign.",
        },
        {
            "brand": "PulseAI",
            "title": "Explainer Video Edit",
            "start": today - timedelta(days=12),
            "end": today + timedelta(days=6),
            "role": "Editor",
            "status": "Active",
            "progress": 60,
            "details": "Editing main explainer + social cuts.",
        },
        {
            "brand": "GreenSpark",
            "title": "Social Reels Series",
            "start": today + timedelta(days=3),
            "end": today + timedelta(days=24),
            "role": "Creator",
            "status": "Pending",
            "progress": 0,
            "details": "Proposal submitted — awaiting brand confirmation.",
        },
    ]


def get_analytics_data() -> Dict[str, Any]:
    """Return analytics datasets: monthly timeseries and demographics."""

    months = pd.date_range(end=pd.Timestamp.today(), periods=12, freq="ME").strftime("%b %Y")
    followers = (np.cumsum(np.random.randint(200, 2000, size=12)) + 20000).astype(int)
    reach = (np.cumsum(np.random.randint(500, 5000, size=12)) + 50000).astype(int)
    impressions = (reach * np.random.uniform(2.5, 4.0, size=12)).astype(int)
    engagement = (np.random.uniform(1.0, 5.0, size=12)).round(2)

    demographics = pd.DataFrame({"age_group": ["18-24", "25-34", "35-44", "45-54", "55+"], "percent": [28, 40, 18, 8, 6]})
    monthly = pd.DataFrame({"month": months, "followers": followers, "reach": reach, "impressions": impressions, "engagement": engagement})

    return {"monthly": monthly, "demographics": demographics}


def get_earnings() -> Dict[str, Any]:
    """Return earnings-related dummy data for `pages.earnings`."""

    months = pd.date_range(end=pd.Timestamp.today(), periods=12, freq="ME").strftime("%b %Y")
    monthly_earnings = pd.Series([1200, 1500, 1700, 1400, 1800, 2200, 2600, 2400, 2700, 3000, 3200, 3500], index=months)

    transactions = [
        {"date": date.today() - timedelta(days=7), "description": "Aurora Labs - final payment", "amount": 1200, "status": "Completed"},
        {"date": date.today() - timedelta(days=20), "description": "PulseAI - milestone 2", "amount": 800, "status": "Completed"},
        {"date": date.today() - timedelta(days=35), "description": "GreenSpark - initial payment", "amount": 600, "status": "Pending"},
    ]

    totals = {"total": int(monthly_earnings.sum()), "pending": 600, "completed": int(monthly_earnings.sum()) - 600}

    return {"totals": totals, "monthly": monthly_earnings, "transactions": transactions}


def get_tasks() -> List[Dict[str, Any]]:
    """Return task list used by `pages.tasks`."""

    today = date.today()
    return [
        {"name": "Edit PulseAI cut", "due": today + timedelta(days=3), "priority": "High", "progress": 40, "completed": False},
        {"name": "Submit Aurora deliverables", "due": today + timedelta(days=15), "priority": "Medium", "progress": 100, "completed": True},
        {"name": "Prepare GreenSpark storyboard", "due": today + timedelta(days=7), "priority": "High", "progress": 10, "completed": False},
    ]


def get_messages() -> Dict[str, Any]:
    """Return messages structure used by `pages.messages`."""

    now = pd.Timestamp.now()
    convs = [
        {
            "id": "c1",
            "name": "Aurora Labs",
            "unread": 0,
            "last_message": "Thanks — got the final files!",
            "messages": [
                {"sender": "Aurora", "text": "Thanks — got the final files!", "ts": now - pd.Timedelta(hours=2)},
                {"sender": "You", "text": "Great — sending invoice.", "ts": now - pd.Timedelta(hours=3)},
            ],
        },
        {
            "id": "c2",
            "name": "PulseAI",
            "unread": 2,
            "last_message": "Can you make the edits by tomorrow?",
            "messages": [
                {"sender": "PulseAI", "text": "Can you make the edits by tomorrow?", "ts": now - pd.Timedelta(minutes=45)},
                {"sender": "You", "text": "Yes, will do.", "ts": now - pd.Timedelta(hours=1)},
            ],
        },
    ]
    return {"conversations": convs}


def get_notifications() -> List[Dict[str, Any]]:
    """Return a small list of notifications for `pages.notifications`."""

    now = pd.Timestamp.now()
    return [
        {"id": "n1", "text": "Payment of $1,200 completed for Aurora Labs", "type": "payment", "ts": now - pd.Timedelta(days=1), "read": False},
        {"id": "n2", "text": "New campaign: GreenSpark wants creators", "type": "campaign", "ts": now - pd.Timedelta(days=2), "read": False},
        {"id": "n3", "text": "Your application to NovaWear was accepted", "type": "application", "ts": now - pd.Timedelta(days=10), "read": True},
    ]
