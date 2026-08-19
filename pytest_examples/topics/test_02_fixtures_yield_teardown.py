"""
Topic: fixtures with setup + teardown via `yield`

Code before `yield` is setup; code after `yield` is teardown. Teardown runs
even if the test fails, because pytest treats it like a `finally` block.

Run:
    python -m pytest pytest_examples/topics/test_02_fixtures_yield_teardown.py -v -s

Example run:
    1 test should PASS. With -s you'll see "[[teardown]] clearing sample_list"
    printed after the test body runs.
"""
import pytest


@pytest.fixture
def sample_list():
    data = [1, 2, 3]        # setup
    yield data
    print("\n[teardown] clearing sample_list")
    data.clear()             # teardown, runs after the test finishes


def test_list_length(sample_list):
    assert len(sample_list) == 3
