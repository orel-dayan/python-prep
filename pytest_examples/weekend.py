"""Code under test for test_mocking_best_practices.py."""

from datetime import datetime


def is_weekend() -> bool:
    return datetime.now().weekday() >= 5  # noqa: DTZ005
