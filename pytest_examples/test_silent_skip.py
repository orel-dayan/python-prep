"""A skipped test is invisible in a green run. Make skips visible.

Run: pytest test_silent_skip.py -rs
The -rs flag prints the reason of every skipped test.
"""

import pytest

SKIP_DB_TESTS = True  # Someone set this in config and forgot about it


def insert_user(user: dict) -> int:
    return 201


@pytest.mark.skipif(SKIP_DB_TESTS, reason="DB connection not available")
def test_user_insert():
    assert insert_user({"name": "alice"}) == 201


def test_user_select():
    assert True
