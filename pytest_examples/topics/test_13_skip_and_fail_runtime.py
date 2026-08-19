"""
Topic: `pytest.skip` / `pytest.fail` called from inside a test body

Imperative alternatives to the `@pytest.mark.skip`/`xfail` decorators, useful
when the decision depends on a runtime condition evaluated inside the test.

Run:
    python -m pytest pytest_examples/topics/test_13_skip_and_fail_runtime.py -v

Example run:
    test_conditional_runtime_skip is SKIPPED, test_manual_fail PASSES
    (flip `valid_state` to False to see pytest.fail in action).
"""
import pytest


def add(a, b):
    return a + b


def test_conditional_runtime_skip():
    feature_enabled = False
    if not feature_enabled:
        pytest.skip("feature not enabled in this environment")
    assert add(1, 1) == 2


def test_manual_fail():
    valid_state = True
    if not valid_state:
        pytest.fail("state was invalid")
    assert True
