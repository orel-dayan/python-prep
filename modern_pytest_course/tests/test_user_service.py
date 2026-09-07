from unittest.mock import MagicMock, patch

import app.user_service

# Records every call as a tuple of (to, subject),
# so the test can verify both the fact of the call AND its exact arguments.
calls = []


def fake_send_email(to, subject):

    calls.append((to, subject))
    return "fake email sent"


def test_register_user_success(mocker):
    mock_send_email = mocker.patch("app.user_service.send_email", return_value=True)
    result = app.user_service.register_user("bob@example.com")
    assert result["status"] == "registered"
    mock_send_email.assert_called_once_with("bob@example.com", "Welcome!")


def test_register_user_failure(mocker):
    mock_send_email = mocker.patch("app.user_service.send_email", return_value=False)
    result = app.user_service.register_user("bob@example.com")
    assert result["status"] == "email_failed"
    mock_send_email.assert_called_once_with("bob@example.com", "Welcome!")


def test_register_user_with_patch():
    with patch("app.user_service.send_email", return_value=True) as mock_send_email:
        result = app.user_service.register_user("bob@example.com")
        assert result["status"] == "registered"
        mock_send_email.assert_called_once_with("bob@example.com", "Welcome!")


# patch with decorator example - patch decorator is applied directly to the test function
# The patch decorator temporarily replaces the target function with a mock during the test.
@patch("app.user_service.send_email", return_value=True)
def test_register_user_with_patch_with_decorator(mock_send_email):
    result = app.user_service.register_user("bob@example.com")
    assert result["status"] == "registered"
    mock_send_email.assert_called_once_with("bob@example.com", "Welcome!")


def test_register_user_sends_email(monkeypatch):
    mock_send_email = MagicMock(return_value=True)
    monkeypatch.setattr(app.user_service, "send_email", mock_send_email)
    result = app.user_service.register_user("colin@example.com")
    assert result["status"] == "registered"
    # register_user calls send_email with keyword arguments, so assert the same way
    mock_send_email.assert_called_once_with("colin@example.com", "Welcome!")


def test_register_user(monkeypatch):
    monkeypatch.setattr(app.user_service, "send_email", fake_send_email)
    result = app.user_service.register_user("dave@example.com")
    # state verification: the result of the function call is as expected
    assert result == {"email": "dave@example.com", "status": "registered"}

    # behavior verification:confirm that the fake_send_email function was called
    # exactly once with the correct arguments
    assert calls == [("dave@example.com", "Welcome!")]


def test_register_user_email_success(monkeypatch):

    def fake_send_email(to, subject):
        return True  # Simulate a successful email send

    monkeypatch.setattr(app.user_service, "send_email", fake_send_email)

    result = app.user_service.register_user("orel@example.com")

    assert result["status"] == "registered"


def test_register_user_email_failure(monkeypatch):

    def fake_send_email(to, subject):
        return False  # Simulate a failed email send

    monkeypatch.setattr(app.user_service, "send_email", fake_send_email)

    result = app.user_service.register_user("avia@example.com")

    assert result["status"] == "email_failed"
