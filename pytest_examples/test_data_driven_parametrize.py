"""Test cases loaded from a CSV file instead of being typed in the code.

Run: pytest test_data_driven_parametrize.py -v
To add a case, add a row to login_attempts.csv. No code change is needed.
"""

import csv
from pathlib import Path

import pytest

from auth import validate_credentials


def load_edge_cases(filename="login_attempts.csv"):
    # Path is relative to this file, so it works from any working directory
    path = Path(__file__).parent / filename
    with path.open(newline="", encoding="utf-8") as f:
        return [
            pytest.param(
                row["username"],
                row["password"],
                int(row["expected_status"]),
                id=f"row{number}",
            )
            for number, row in enumerate(csv.DictReader(f), start=1)
        ]


@pytest.mark.parametrize("user, pw, expected", load_edge_cases())
def test_login_validation(user, pw, expected):
    assert validate_credentials(user, pw) == expected
