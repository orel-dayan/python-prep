import json
import time
from pathlib import Path


class FakeFileDatabase:
    def __init__(self, file_path:Path):
        print("Creating fake file database...")
        time.sleep(1)

        self.file_path = file_path
        self._write_initial_data()

    def _write_initial_data(self):
        data = {
            "users": {
                "1": "Alice",
                "2": "Bob",
                "3": "Charlie",
            }
        }
        self.file_path.write_text(json.dumps(data))

    def get_user(self, user_id):
        data = json.loads(self.file_path.read_text())
        return data["users"].get(user_id)
