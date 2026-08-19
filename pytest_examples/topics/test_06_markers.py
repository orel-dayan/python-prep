"""
Topic: markers - smoke, slow, skip, skipif, xfail

Markers tag tests with metadata, used for selection (`-m`) or special
behavior. Custom markers (`smoke`, `slow`) must be registered in the repo
root `pytest.ini`'s `markers =` section, or pytest emits a warning.

Run:
    python -m pytest pytest_examples/topics/test_06_markers.py -v
    python -m pytest pytest_examples/topics/test_06_markers.py -m smoke -v   # only smoke tests

Example run:
    5 tests total: test_add_smoke and test_conditional_skip PASS (Python 3.8+),
    test_future_feature is SKIPPED, test_known_bug is XFAIL (expected
    failure). test_heavy_computation is also SKIPPED by default - the repo
    root conftest.py auto-skips @pytest.mark.slow tests unless --runslow is
    passed.
"""
import sys
import time

import pytest


def add(a, b):
    return a + b


@pytest.mark.smoke
def test_add_smoke():
    assert add(1, 1) == 2


@pytest.mark.slow
def test_heavy_computation():
    time.sleep(0.1)  # simulates a slow operation
    assert add(2, 2) == 4


@pytest.mark.skip(reason="not implemented yet")
def test_future_feature():
    ...


@pytest.mark.skipif(sys.version_info < (3, 8), reason="requires Python 3.8+")
def test_conditional_skip():
    assert add(1, 2) == 3


@pytest.mark.xfail(reason="known bug - demonstrates a failing assertion")
def test_known_bug():
    assert add(1, 1) == 1
