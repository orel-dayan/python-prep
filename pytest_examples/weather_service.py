"""Code under test for test_mocking_best_practices.py."""

import requests


class WeatherService:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_temperature(self, city: str) -> float:
        response = requests.get(
            f"https://api.weather.com/v1/{city}",
            headers={"X-Api-Key": self.api_key},
            timeout=10,
        )
        return response.json()["temperature"]
