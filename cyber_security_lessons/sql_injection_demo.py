"""
Demo: SQL Injection vs Parameterized Queries
Uses an in-memory SQLite database so it can run standalone, no setup needed.
"""

import sqlite3


def setup_fake_db():
    """Create an in-memory database with a users table and some sample data."""
    connection = sqlite3.connect(":memory:")
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT
        )
    """)
    cursor.executemany(
        "INSERT INTO users (id, username, password) VALUES (?, ?, ?)",
        [
            (1, "alice", "alice_secret"),
            (2, "bob", "bob_secret"),
            (3, "admin", "super_secret_admin_pw"),
        ],
    )
    connection.commit()
    return connection


def get_user_bad(connection, user_id):
    """VULNERABLE: builds the SQL string by directly inserting user input."""
    cursor = connection.cursor()
    query = f"SELECT * FROM users WHERE id = {user_id}"
    print(f"  [bad]  actual SQL sent to DB: {query}")
    cursor.execute(query)
    return cursor.fetchall()


def get_user_safe(connection, user_id):
    """SAFE: uses a parameterized query (placeholder + separate value)."""
    cursor = connection.cursor()
    query = "SELECT * FROM users WHERE id = ?"
    print(f"  [safe] query sent to DB:      {query}   (value bound separately: {user_id!r})")
    cursor.execute(query, (user_id,))
    return cursor.fetchall()




if __name__ == "__main__":
    connection = setup_fake_db()
    
    print("=== Normal usage (both work the same) ===")
    print("bad :", get_user_bad(connection, "1"))
    print("safe:", get_user_safe(connection, "1"))
    
    malicious_input = "1 OR 1=1"
    
    print("\n=== Malicious input: user_id = '1 OR 1=1' ===")
    print("bad :", get_user_bad(connection, malicious_input))
    print("      ^ leaked ALL users, including admin's password!\n")
    
    print("safe:", get_user_safe(connection, malicious_input))
    print("      ^ no match found, input was treated as a plain value, not SQL")
    
    connection.close()