"""Basic tests for data providers in `data/dummy_data.py`.

These tests ensure the dummy data functions return objects with expected
shapes. They are intentionally lightweight and suitable for CI checks.
"""

from data import dummy_data


def test_dashboard_provider():
    data = dummy_data.get_dashboard_data()
    assert "metrics" in data
    assert "monthly_earnings" in data
    assert hasattr(data["monthly_earnings"], "values")


def test_profile_provider():
    p = dummy_data.get_profile_data()
    assert "name" in p and "bio" in p
