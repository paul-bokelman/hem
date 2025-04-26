# tool_runners.py
import requests
import os

def get_weather(location: str) -> str:
    """Fetches the current weather for a given location using OpenWeatherMap API."""
    api_key = os.environ.get("OPEN_WEATHER_API_KEY")
    if not api_key:
        raise ValueError("API key for OpenWeatherMap is not set.")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=imperial"
    response = requests.get(url)
    data = response.json()
    temp_f = data["main"]["temp"]
    condition = data["weather"][0]["description"]
    return f"{temp_f}°F and {condition}."
