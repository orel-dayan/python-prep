"""Mocking with pytest-mock. Golden rule: patch the name where it is USED.

Run: pytest test_mocking_best_practices.py -v
Needs: pip install pytest-mock requests
"""

import datetime as dt
from unittest.mock import MagicMock

import weather_service
import weekend
from weather_service import WeatherService


def test_get_temperature_mocks_correctly(mocker):
    # weather_service.py does "import requests", so we patch the name
    # "requests" as seen from the weather_service module.
    mock_get = mocker.patch("weather_service.requests.get")
    mock_response = MagicMock()
    mock_response.json.return_value = {"temperature": 22}
    mock_get.return_value = mock_response

    temp = WeatherService(api_key="test_key").get_temperature("London")

    assert temp == 22
    mock_get.assert_called_once_with(
        "https://api.weather.com/v1/London",
        headers={"X-Api-Key": "test_key"},
        timeout=10,
    )


def test_is_weekend_with_mock(mocker):
    # weekend.py does "from datetime import datetime", so the module owns a
    # name "datetime". That is the name we patch: "weekend.datetime".
    mock_datetime = mocker.patch("weekend.datetime")
    # Use the real class through the alias "dt": the name "datetime" is
    # not needed in this test file at all.
    mock_datetime.now.return_value = dt.datetime(2025, 5, 10)  # noqa: DTZ001  Saturday
    assert weekend.is_weekend() is True


def test_patching_the_original_has_no_effect(mocker):
    # WRONG target: we patch where datetime is defined, not where it is used.
    mock_original = mocker.patch("datetime.datetime")
    weekend.is_weekend()
    # weekend.py still uses its own reference, so the mock was never called
    mock_original.now.assert_not_called()


def test_spy_on_function_call(mocker):
    service = WeatherService(api_key="test")
    spy = mocker.spy(service, "get_temperature")
    mocker.patch("weather_service.requests.get")
    service.get_temperature("Paris")
    spy.assert_called_once_with("Paris")


def test_module_attribute_is_really_replaced(mocker):
    mock_get = mocker.patch("weather_service.requests.get")
    assert weather_service.requests.get is mock_get
