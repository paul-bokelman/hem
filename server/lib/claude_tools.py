# claude_tools.py

import os
from typing import Any, Callable, Tuple
import requests
from dotenv import load_dotenv
from urllib.parse import quote_plus
from datetime import datetime
import json

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

@tool(
    name="get_time",
    description=(
        "Retrieves the current local time in HH:MM:SS format based on the system's local timezone. "
        "Use this tool whenever a user asks for the current time without specifying a different timezone. "
        "It assumes the server clock is correctly synchronized and does not account for user-specific timezone requests. "
        "Returns the time as a string in 24-hour format (e.g., 14:23:05)."
    ),
    input_schema={
        "type": "object",
        "properties": {},
        "required": []
    }
)
def get_time() -> str:
    """
    Returns the current local time in HH:MM:SS format.
    """
    now = datetime.now()
    return now.strftime("%H:%M:%S")


@tool(
    name="get_weather",
    description=(
        "Retrieves the current weather and short-term forecast for a given city and state. "
        "Use this tool whenever a user requests weather information for a specific location, including temperature, conditions, and forecast ranges. "
        "The input location must be formatted as 'City' (e.g., 'Austin') and will be geocoded to latitude/longitude internally. "
        "This tool depends on the OpenWeatherMap API and assumes the API key is set correctly. It may fail if the city name is misspelled or invalid."
    ),
    input_schema={
        "type": "object",
        "properties": {
            "location": {"type": "string", "description": "City, e.g., 'Boise'"}
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

@tool(
    name="get_stock_info",
    description="Retrieves current stock prices and related financial data for a list of provided stock tickers. Use when a user provides one or more stock symbols (e.g., ['AAPL', 'GOOG']). This tool fetches live stock market information and summarizes it for quick reference. Ticker symbols must be accurate as the tool does not auto-correct invalid inputs.",
    input_schema={
        "type": "object",
        "properties": {
            "tickers": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of stock ticker symbols, e.g., ['AAPL', 'TSLA']."
            }
        },
        "required": ["tickers"]
    }
)
def get_stock_info(tickers: list[str]) -> str:
    api_key = os.getenv("MARKET_STACK_API_KEY")

    url = "http://api.marketstack.com/v2/eod" + "?access_key=" + api_key + "&symbols=" 
    url += ",".join(tickers)
    url += "&limit=1"
    

    response = requests.get(url)
    data = response.json()
    return data

@tool(
    name="get_crypto_price",
    description=(
        "Retrieves live cryptocurrency market data for a specific coin ID (such as 'bitcoin', 'ethereum') "
        "in a specified fiat currency (such as 'USD', 'EUR', 'AMD'). "
        "Uses the public Coingecko API (no authentication required). "
        "Returns current price, market cap, 24h volume, and other metadata for the coin."
    ),
    input_schema={
        "type": "object",
        "properties": {
            "coin": {
                "type": "string",
                "description": "The ID of the cryptocurrency on Coingecko (e.g., 'bitcoin', 'ethereum', 'dogecoin')."
            },
            "currency": {
                "type": "string",
                "description": "The fiat currency code (e.g., 'usd', 'eur', 'amd')."
            }
        },
        "required": ["coin", "currency"]
    }
)
def get_crypto_price(coin: str, currency: str) -> dict:
    """
    Fetches the live cryptocurrency price and metadata from Coingecko.
    """
    url = (
        "https://api.coingecko.com/api/v3/coins/markets"
        f"?vs_currency={quote_plus(currency)}&ids={quote_plus(coin)}"
    )
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        raise ValueError(f"Network error fetching crypto data: {e}")

    data = resp.json()

    if not data:
        raise ValueError(f"No data found for coin '{coin}' in currency '{currency}'.")

    return data[0]  # Coingecko returns a list



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