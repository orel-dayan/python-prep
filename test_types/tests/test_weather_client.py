from unittest.mock import MagicMock


def test_get_temperature_returns_value():
    api_mock = MagicMock()
    api_mock.fetch.return_value = {"temp": 25.0}