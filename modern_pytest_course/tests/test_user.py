import pytest
from app.user import format_email


def test_format_email_removes_whitespace():
    result = format_email("  test@example.com  ")
    assert result == "test@example.com"
    
    
def test_format_email_lowercases():
    result = format_email("TEST@EXAMPLE.COM")
    assert result == "test@example.com"
    
    
def test_email_normalization():
    result = format_email("  TEST@EXAMPLE.COM  ")
    assert result.startswith("test")
    assert "@" in result
    
    
def test_format_email_invalid():
    with pytest.raises(ValueError,match="^Invalid email"):
        format_email("not an email")
    
