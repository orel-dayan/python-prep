"""
Topic: mocking with `unittest.mock` (`Mock` + `patch`)

`Mock()` creates a fake object that records how it was called and returns
canned values, so you can test code in isolation from a real dependency
(here: an email "sender"). `@patch(...)` temporarily replaces a real
object/function for the duration of the test.

Run:
    python -m pytest pytest_examples/topics/test_09_mocking_unittest_mock.py -v

Example run:
    2 tests should PASS.
"""
from unittest.mock import Mock, patch


def notify_user(email, sender):
    # "sender" is an injected dependency (e.g. a real email service)
    return sender.send(email)


def test_with_mock_object():
    fake_sender = Mock()
    fake_sender.send.return_value = True

    result = notify_user("test@example.com", fake_sender)

    assert result is True
    fake_sender.send.assert_called_once_with("test@example.com")


@patch("builtins.print")
def test_patch_builtin(mock_print):
    print("hello")
    mock_print.assert_called_once_with("hello")
