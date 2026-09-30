"""Tests that FAIL ON PURPOSE. They are not collected by a plain "pytest".

Run: pytest traps/trap_shared_state.py -v -p no:randomly
"""

import pytest

# --- Trap 1: mutable fixture with session scope ---


@pytest.fixture(scope="session")
def user_ids():
    return [1, 2, 3]  # One single list shared by ALL tests


def test_a_appends_an_id(user_ids):
    user_ids.append(4)
    assert len(user_ids) == 4


def test_b_expects_three_ids(user_ids):
    # Fails: test_a changed the shared list. Alone, this test passes.
    assert len(user_ids) == 3


# --- Trap 2: hidden dependency through module-level state ---

_cache: dict = {}


def test_c_fills_the_cache():
    _cache["key"] = "value"


def test_d_expects_empty_cache():
    # Fails when test_c ran first. Alone, this test passes.
    assert _cache == {}
