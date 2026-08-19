import pytest
from string_utils import count_words, is_palindrome, reverse_text, truncate


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("abc", "cba"),
        ("Python", "nohtyP"),
        ("", ""),
    ],
)
def test_reverse_text_returns_reversed(text, expected):
    assert reverse_text(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("hello world", 2),
        ("hello big world", 3),
        ("", 0),
    ],
)
def test_count_words_returns_count(text, expected):
    assert count_words(text) == expected


@pytest.mark.parametrize("text", ["aba", "Aba", "never odd or even", "a", ""])
def test_is_palindrome_returns_true(text):
    assert is_palindrome(text) is True


@pytest.mark.parametrize("text", ["abc", "hello", "ab ba c"])
def test_is_palindrome_returns_false(text):
    assert is_palindrome(text) is False


@pytest.mark.parametrize(
    ("text", "max_length", "expected"),
    [
        ("hello", 10, "hello"),
        ("hello", 5, "hello"),
        ("hello", 4, "hell..."),
        ("hello", 1, "h..."),
    ],
)
def test_truncate_returns_expected(text, max_length, expected):
    assert truncate(text, max_length) == expected


def test_truncate_raises_on_zero_length():
    with pytest.raises(ValueError, match="max_length must be at least 1"):
        truncate("hello", 0)


def test_truncate_raises_on_negative_length():
    with pytest.raises(ValueError, match="max_length must be at least 1"):
        truncate("hello", -5)