import os
import sys

# ============================================================
# USE MONKEYPATCH FOR: Environment variables, sys.argv, builtins
# ============================================================

def get_database_url():
    return os.environ.get("DATABASE_URL", "sqlite:///default.db")

def test_monkeypatch_env_var(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://prod")
    assert get_database_url() == "postgresql://prod"

def is_test_mode():
    return sys.argv[0].endswith("pytest")

def test_monkeypatch_sys_argv(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["pytest", "test.py"])
    assert is_test_mode() is True

# ============================================================
# USE MOCKER FOR: Call assertions, return values, exceptions
# ============================================================

class EmailSender:
    def send(self, to, message):
        pass

def notify_customer(email_sender, customer_email):
    email_sender.send(customer_email, "Your order shipped!")

def test_mocker_asserts_call(mocker):
    mock_sender = mocker.Mock(spec=EmailSender) # spec ensures only methods of EmailSender can be called
    notify_customer(mock_sender, "customer@example.com")
    mock_sender.send.assert_called_once_with(
        "customer@example.com", "Your order shipped!"
    )

# Comparison table
# | Feature                          | mocker (pytest-mock) | monkeypatch |
# |----------------------------------|-----------------------|-------------|
# | Assert call count & arguments    | Yes (assert_called_*) | No          |
# | Control return value             | Yes (return_value)    | Replace     |
# | Raise exceptions                 | Yes (side_effect)     | Replace     |
# | Modify environment variables     | No (use monkeypatch)  | Yes         |
# | Replace builtins (open, input)   | Limited               | Yes         |
# | Spying on existing functions     | Yes (spy)             | No          |
# | Autoreset after test             | Yes                   | Yes         |
# | Module-level attributes          | Yes (patch)           | Yes         |