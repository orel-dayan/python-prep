"""Simple string utilities for pytest practice."""


def reverse_text(text):
    """Return the text reversed."""
    return text[::-1]


def count_words(text):
    """Return the number of words in the text."""
    return len(text.split())


def is_palindrome(text):
    """Return True if the text reads the same backwards, ignoring case and spaces."""
    cleaned = text.replace(" ", "").lower()
    return cleaned == cleaned[::-1]


def truncate(text, max_length):
    """Return the text shortened to max_length, adding '...' if it was cut."""
    if max_length < 1:
        raise ValueError("max_length must be at least 1")
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."