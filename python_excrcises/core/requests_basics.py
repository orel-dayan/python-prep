"""requests — the sync HTTP client cheat sheet.

For an async client with retries and Pydantic validation, see
automation_examples/network/api_client.py.
"""

import requests

BASE_URL = "https://httpbin.org"


def get_json(path: str) -> dict:
    response = requests.get(f"{BASE_URL}/{path}", timeout=5)
    response.raise_for_status()  # raises HTTPError on 4xx/5xx instead of failing silently
    return response.json()


def post_json(path: str, payload: dict) -> dict:
    response = requests.post(f"{BASE_URL}/{path}", json=payload, timeout=5)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    try:
        data = get_json("get")
        print("GET  ok, origin:", data["origin"])

        data = post_json("post", {"name": "test"})
        print("POST ok, echoed:", data["json"])
    except requests.RequestException as e:
        print(f"network call failed: {e}")
