"""
Unit tests for weather.py using mocked HTTP responses.
Run with: pytest tests/
"""

from unittest.mock import MagicMock, patch

import pytest

from lambda.weather import get_weather


MOCK_RESPONSE = {
    "main": {
        "temp": 72.5,
        "temp_max": 80.1,
        "temp_min": 65.3,
        "humidity": 55,
    },
    "weather": [{"description": "clear sky", "main": "Clear"}],
}


@patch("lambda.weather.requests.get")
def test_get_weather_returns_expected_keys(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = MOCK_RESPONSE
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = get_weather(api_key="fake-key", city="Los Angeles")

    assert result["city"] == "Los Angeles"
    assert result["temp_current"] == 73  # rounded from 72.5
    assert result["temp_high"] == 80
    assert result["temp_low"] == 65
    assert result["description"] == "Clear Sky"  # .title() applied
    assert result["humidity"] == 55
    assert result["icon"] == "Clear"


@patch("lambda.weather.requests.get")
def test_get_weather_raises_on_bad_response(mock_get):
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = Exception("404 Not Found")
    mock_get.return_value = mock_response

    with pytest.raises(Exception, match="404 Not Found"):
        get_weather(api_key="bad-key")
