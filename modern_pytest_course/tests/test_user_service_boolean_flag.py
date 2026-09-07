import app.user_service

"""
This test module demonstrates how to use monkeypatching to replace a function in the user_service module with a fake implementation for testing purposes.
"""
#  tracks whether the fake_send_email function was called
state = {"called": False}


def fake_send_email(to, subject):
    # record only the fact that a call happened
    # not what the arguments were
    # since we don't care about them in this test
    state["called"] = True
    return "fake email sent"


def test_register_user(monkeypatch):
    monkeypatch.setattr(app.user_service, "send_email", fake_send_email)
    result = app.user_service.register_user("dave@example.com")
    assert result == {"email": "dave@example.com", "status": "registered"}

    # Now catches the "forgot to call send_email" bug
    # Problem : still does not verify *what* was sent, just that something was sent
    # A bug like send_email(wrong_email, "Welcome!") would still pass this assertion
    assert state["called"]
