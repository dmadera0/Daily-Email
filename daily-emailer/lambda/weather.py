import requests


def get_weather(api_key: str, city: str = "Los Angeles") -> dict:
    """
    Fetches current weather from OpenWeatherMap free tier API.

    Args:
        api_key: OpenWeatherMap API key from Secrets Manager
        city: City name string, defaults to Los Angeles

    Returns:
        dict with keys: city, temp_current, temp_high, temp_low,
                        description, humidity, icon
    """
    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": api_key,
        "units": "imperial",  # Fahrenheit
    }

    response = requests.get(url, params=params, timeout=5)
    response.raise_for_status()

    data = response.json()

    return {
        "city": city,
        "temp_current": round(data["main"]["temp"]),
        "temp_high": round(data["main"]["temp_max"]),
        "temp_low": round(data["main"]["temp_min"]),
        "description": data["weather"][0]["description"].title(),
        "humidity": data["main"]["humidity"],
        "icon": data["weather"][0]["main"],  # e.g. "Clear", "Rain", "Clouds"
    }
