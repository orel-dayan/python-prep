import pytest
from app.validation import is_valid_email


@pytest.mark.parametrize(
    "email, expected",
    [
        ("alice@example.com", True),
        ("alice.smith@example.com", True),
        ("alice-example.com", False),
        ("alice@", False),
        ("", False),
        ("ALICE@EXAMPLE.COM", True)
    ]
)
def test_is_valid_email(email, expected):
    assert is_valid_email(email) == expected
