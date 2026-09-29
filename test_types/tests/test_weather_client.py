from unittest.mock import MagicMock, patch, call

import pytest
from weather_client import WeatherClient, WeatherError


@pytest.fixture
def api():
    """Provide a mock weather API."""
    return MagicMock()


@pytest.fixture
def client(api):
    """Provide a WeatherClient backed by the mock API."""
    return WeatherClient(api)

@pytest.fixture(autouse=True)
def patch_time_sleep():
    with patch("weather_client.time.sleep"):
        yield

def test_get_temperature_returns_value(api, client):
    api.fetch.return_value = {"temp": 25.0}
    assert client.get_temperature("Tel Aviv") == 25.0


def test_get_temperature_calls_api_with_city(api, client):
    api.fetch.return_value = {"temp": 25.0}
    client.get_temperature("Tel Aviv")
    api.fetch.assert_called_once_with("Tel Aviv")


def test_get_temperature_succeeds_on_third_attempt(api, client):
    api.fetch.side_effect = [ConnectionError(), ConnectionError(), {"temp": "10"}]
    assert client.get_temperature("Tel Aviv") == 10.0
    assert api.fetch.call_count == 3


def test_get_temperature_raises_after_all_retries(api, client):
    api.fetch.side_effect = ConnectionError()
    with patch("weather_client.time.sleep"), pytest.raises(WeatherError):
        client.get_temperature("Tel Aviv")
    assert api.fetch.call_count == 3


def test_retries_count_is_configurable(api):
    api.fetch.side_effect = ConnectionError()
    client = WeatherClient(api, retries=5)
    
    with patch("weather_client.time.sleep"), pytest.raises(WeatherError):
        client.get_temperature("Tel Aviv")
    assert api.fetch.call_count == 5

def test_retry_delays_grow_between_attempts(api, client):
    api.fetch.side_effect = ConnectionError()

    with patch("weather_client.time.sleep") as mock_sleep:  # noqa: SIM117
        with pytest.raises(WeatherError):
            client.get_temperature("Tel Aviv")

    assert mock_sleep.call_args_list == [call(2.0), call(4.0), call(6.0)]

@pytest.mark.parametrize(
    ("temperature", "expected"),
    [(-25, True), (-1, True), (0, True), (0.5, False), (1, False), (10, False)],
)
def test_is_freezing(api, client, temperature, expected):
    api.fetch.return_value = {"temp": temperature}
    assert client.is_freezing("Tel Aviv") is expected


@pytest.mark.xfail(
    reason="BUG-03: malformed response leaks KeyError instead of WeatherError"
)
def test_get_temperature_raises_weather_error_on_missing_key(api, client):
    api.fetch.return_value = {"humidity": 80}
    with pytest.raises(WeatherError):
        client.get_temperature("Tel Aviv")


@pytest.mark.xfail(
    reason="BUG-04: malformed response leaks ValueError instead of WeatherError"
)
def test_get_temperature_raises_weather_error_on_non_numeric(api, client):
    api.fetch.return_value = {"temp": "not_a_number"}
    with pytest.raises(WeatherError):
        client.get_temperature("Tel Aviv")
