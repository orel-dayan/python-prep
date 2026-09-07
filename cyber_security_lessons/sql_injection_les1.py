"""
Demo: the SAME injection idea, but with NO real database or SQL at all.
The "database" is just a Python list of dicts.
The "bad" version turns user input into CODE (like building a SQL string).
The "safe" version only ever treats user input as a plain VALUE.
"""

fake_db = [
    {"id": 1, "username": "alice", "password": "alice_secret"},
    {"id": 2, "username": "bob", "password": "bob_secret"},
    {"id": 3, "username": "admin", "password": "super_secret_admin_pw"},
]


def get_user_bad(user_id):
    """VULNERABLE: builds a Python expression as text and executes it.

    This mirrors building a SQL string with f-strings: the input becomes
    part of the CODE that runs, not just a value being compared.
    """
    results = []
    for row in fake_db:
        condition = f"row['id'] == {user_id}"
        if eval(condition, {"row": row}):  # intentionally unsafe, for demo only
            results.append(row)
    print(f"  [bad]  condition executed per row: row['id'] == {user_id}")
    return results


def get_user_safe(user_id):
    """SAFE: user_id is only ever compared as plain data, never turned into code."""
    try:
        target_id = int(user_id)
    except ValueError:
        print(f"  [safe] input {user_id!r} rejected - not a valid id, no code involved")
        return []
    print(f"  [safe] comparing row['id'] == {target_id} (plain value, not code)")
    return [row for row in fake_db if row["id"] == target_id]


if __name__ == "__main__":
    print("=== Normal usage (both work the same) ===")
    print("bad :", get_user_bad("1"))
    print("safe:", get_user_safe("1"))

    malicious_input = "1 or True"  # Python's version of SQL's "OR 1=1"

    print(f"\n=== Malicious input: user_id = {malicious_input!r} ===")
    print("bad :", get_user_bad(malicious_input))
    print("      ^ leaked ALL users, including admin's password!\n")

    print("safe:", get_user_safe(malicious_input))
    print("      ^ rejected safely, nothing leaked")