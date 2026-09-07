import time


def fast_sum(numbers):
    """Returns the sum of a list of numbers."""
    return sum(numbers)


def slow_report(data):
    """Returns a report of the sum of a list of numbers, but is intentionally slow."""
    time.sleep(2)  # simulate a slow operation
    return {
        "count": len(data),
        "sum": sum(data),
        "mean": sum(data) / len(data) if data else 0,
    }
