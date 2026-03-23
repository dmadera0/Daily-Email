from lambda.email_builder import build_email_html, get_weather_icon


def test_weather_icon_known_key():
    assert get_weather_icon("Clear") == "☀️"
    assert get_weather_icon("Rain") == "🌧️"
    assert get_weather_icon("Snow") == "❄️"


def test_weather_icon_unknown_key():
    assert get_weather_icon("Tornado") == "🌡️"


def test_build_email_html_contains_key_content():
    weather = {
        "city": "Los Angeles",
        "temp_current": 75,
        "temp_high": 82,
        "temp_low": 64,
        "description": "Sunny",
        "humidity": 40,
        "icon": "Clear",
    }
    news = [
        {
            "title": "Test headline",
            "source": "Test News",
            "url": "https://example.com",
            "description": "A test article.",
        }
    ]
    quote = {"quote": "Keep going.", "author": "Unknown"}

    html = build_email_html(weather, news, quote)

    assert "Los Angeles" in html
    assert "75" in html
    assert "Test headline" in html
    assert "Keep going." in html
    assert "Unknown" in html
    assert "Good Morning" in html
