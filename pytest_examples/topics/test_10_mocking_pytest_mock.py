"""
Topic: mocking with pytest-mock (the `mocker` fixture)

pytest-mock wraps `unittest.mock.patch` in a `mocker` fixture, so patches are
automatically undone after the test - no `with patch(...):` block needed.

Requires: pytest-mock (already installed in this project's .venv). Without it,
this test errors with "fixture 'mocker' not found".

Run:
    python -m pytest pytest_examples/topics/test_10_mocking_pytest_mock.py -v

Example run:
    1 test should PASS.
"""


def notify_user(email, sender):
    return sender.send(email)


def test_with_mocker(mocker):
    mock_sender = mocker.Mock()
    mock_sender.send.return_value = True

    result = notify_user("test@example.com", mock_sender)

    assert result is True
    mock_sender.send.assert_called_once()
