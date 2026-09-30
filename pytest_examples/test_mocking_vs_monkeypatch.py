"""mocker (verify behavior) vs monkeypatch (change state).

Run: pytest test_mocking_vs_monkeypatch.py -v
"""

import os
import sys


def get_database_url():
    return os.environ.get("DATABASE_URL", "sqlite:///default.db")


def test_monkeypatch_env_var(monkeypatch):
    # monkeypatch: temporary state change, restored automatically
    monkeypatch.setenv("DATABASE_URL", "postgresql://prod")
    assert get_database_url() == "postgresql://prod"


def test_env_var_is_restored_after_previous_test():
    assert os.environ.get("DATABASE_URL") != "postgresql://prod"


def is_test_mode():
    return sys.argv[0].endswith("pytest")


def test_monkeypatch_sys_argv(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["pytest", "test.py"])
    assert is_test_mode() is True


class EmailSender:
    def send(self, to, message):
        pass


def notify_customer(email_sender, customer_email):
    email_sender.send(customer_email, "Your order shipped!")


def test_mocker_asserts_call(mocker):
    # mocker: we care HOW the dependency was used (call count and arguments)
    mock_sender = mocker.Mock(spec=EmailSender)
    notify_customer(mock_sender, "customer@example.com")
    mock_sender.send.assert_called_once_with(
        "customer@example.com", "Your order shipped!"
    )
