"""
Topic: `Mock(spec=...)` / `create_autospec` — catching typos in your mocks

A plain `Mock()` has no idea what the real object looks like, so it happily
accepts ANY attribute or method name - `fake.sedn(...)` (a typo for `send`)
silently returns another Mock instead of erroring, and the test passes for
the wrong reason. `spec`/`autospec` restrict the mock to the real object's
actual interface, so that typo raises AttributeError immediately, the same
error you'd get calling it on the real class.

Run:
    python -m pytest pytest_examples/topics/test_18_mock_spec_and_autospec.py -v

Example run:
    2 tests should PASS.
"""
from unittest.mock import Mock, create_autospec

import pytest


class Sender:
    def send(self, email: str) -> bool:
        raise NotImplementedError("real implementation would call an email API")


def test_plain_mock_lets_a_typo_through():
    fake = Mock()
    fake.sedn("a@example.com")  # typo for send() - no error, no warning
    assert fake.sedn.called  # "passes", but it tested nothing real


def test_autospec_catches_the_same_typo():
    fake = create_autospec(Sender, instance=True)
    fake.send("a@example.com")  # matches the real signature - fine

    with pytest.raises(AttributeError):
        fake.sedn("a@example.com")  # not a real Sender method - caught immediately
