"""Fetches temperature data from an external service."""


class WeatherError(Exception):
    """Raised when the weather service cannot be reached."""


class WeatherClient:
    def __init__(self, api, retries=3):
        self.api = api
        self.retries = retries

    def get_temperature(self, city):
        """Return the temperature for a city, retrying on failure."""
        last_error = None
        for _ in range(self.retries):
            try:
                raw = self.api.fetch(city)
                return float(raw["temp"])
            except ConnectionError as exc:
                last_error = exc
        raise WeatherError(f"failed after {self.retries} attempts: {last_error}")

    def is_freezing(self, city):
        """Return True if the temperature is at or below zero."""
        return self.get_temperature(city) <= 0