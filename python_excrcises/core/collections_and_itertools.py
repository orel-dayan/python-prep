"""Counter and groupby — the two collections/itertools tools used most often
when summarizing logs or scan results.
"""

import itertools
from collections import Counter

LOG_LINES = [
    ("web-01", "ERROR", "disk full"),
    ("web-01", "INFO", "started"),
    ("db-01", "ERROR", "connection refused"),
    ("web-02", "WARN", "high memory"),
    ("db-01", "ERROR", "timeout"),
]


def count_by_level(lines: list[tuple[str, str, str]]) -> Counter:
    """How many log lines fall into each level."""
    return Counter(level for _, level, _ in lines)


def group_by_host(lines: list[tuple[str, str, str]]) -> dict[str, list[str]]:
    """groupby only groups CONSECUTIVE items, so sort by the key first."""
    rows = sorted(lines, key=lambda r: r[0])
    return {
        host: [msg for _, _, msg in group]
        for host, group in itertools.groupby(rows, key=lambda r: r[0])
    }


if __name__ == "__main__":
    print(count_by_level(LOG_LINES).most_common())
    print(group_by_host(LOG_LINES))
