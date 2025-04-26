# claude_tools.py
# claude_tools.py

import os
from typing import Any, Callable, Tuple
import requests
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

# Decorator to attach metadata to functions as tools
def tool(name: str, description: str, input_schema: dict):
    """
    Decorator to attach tool metadata to functions.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func.__tool__ = {
            "name": name,
            "description": description,
            "input_schema": input_schema,
        }
        return func
    return decorator

# Internal helper: geocode a city to lat/lon
def _geocode(city: str) -> Tuple[float, float]:
    """
    Helper: Convert a city name into (lat, lon) via OpenStreetMap Nominatim.
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": city, "format": "json", "limit": 1}
    headers = {"User-Agent": "claude-tools/1.0"}
    resp = requests.get(url, params=params, headers=headers, timeout=5)
    resp.raise_for_status()
    results = resp.json()
    if not results:
        raise ValueError(f"Could not geocode city '{city}'")
    lat = float(results[0]["lat"])
    lon = float(results[0]["lon"])
    return lat, lon

@tool(
    name="get_weather",
    description="Retrieves current weather and forecast for a given city.",
    input_schema={
        "type": "object",
        "properties": {
            "location": {"type": "string", "description": "City and state, e.g. 'Austin, TX'"}
        },
        "required": ["location"]
    }
)
def get_weather(location: str) -> str:
    """
    Fetches current weather and daily forecast for the provided city.
    """
    api_key = os.environ.get("OPEN_WEATHER_API_KEY")
    if not api_key:
        raise ValueError("API key for OpenWeatherMap is not set.")

    # Geocode the location to latitude/longitude
    lat, lon = _geocode(location)

    # Call OpenWeather One Call API for current and forecast data
    url = (
        f"https://api.openweathermap.org/data/3.0/onecall"
        f"?lat={lat}&lon={lon}&appid={api_key}&units=imperial"
    )
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        raise ValueError(f"Network error fetching weather data: {e}")

    data = resp.json()

    # Extract current conditions
    current = data.get("current", {})
    temp = current.get("temp")
    weather = current.get("weather", [])
    desc = weather[0].get("description") if weather else "no description"

    # Extract today's forecast (min/max)
    daily = data.get("daily", [])
    if daily:
        today = daily[0].get("temp", {})
        min_temp = today.get("min")
        max_temp = today.get("max")
        return (
            f"{location.title()}: {desc}, {temp:.1f}°F "
            f"(min {min_temp:.1f}°F, max {max_temp:.1f}°F)"
        )
    else:
        return f"{location.title()}: {desc}, {temp:.1f}°F"