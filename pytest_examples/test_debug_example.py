"""Dropping into the debugger, guarded by an environment variable.

Normal run:  pytest test_debug_example.py
Debug run (PowerShell): $env:PDB_ENABLED = "1"; pytest test_debug_example.py -s
Debug on failure: pytest test_debug_example.py --pdb
"""

import os


def fetch_data():
    return {"items": [1, 2, 3]}


def process(data):
    return {"status": "ok", "count": len(data["items"])}


def test_process_order():
    data = fetch_data()
    if os.getenv("PDB_ENABLED"):
        # Guarded, so a forgotten breakpoint can never hang CI
        breakpoint()  # noqa: T100
    result = process(data)
    assert result["status"] == "ok"
