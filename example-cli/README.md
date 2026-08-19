# Example CLI

A small example CLI application that fetches user data (from `jsonplaceholder.typicode.com` or
a local example list) and stores/deletes per-user JSON files on disk.

## Files

- `main.py` — Core logic: `get_example_users()` (hardcoded sample users), `get_real_users()`
  (fetches users via `httpx` from the JSONPlaceholder API), `create_user_file()` (writes a
  user's data to a JSON file under `users/`), and `delete_user_files()` (removes JSON files for
  users not in a given keep-list).
- `test_main.py` — Tests exercising `get_real_users`, `create_user_file`, and `delete_user_files`
  against the `users/` folder.
- `users/` — Sample per-user JSON files, named `<id>_<FirstName>_<LastName>.json`
  (e.g. `001_Bret_Leanne.json`).

## Running

```powershell
python -m pytest example-cli
```
