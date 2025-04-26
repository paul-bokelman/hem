from typing import cast, Callable, Union, Tuple
from urllib.parse import quote_plus
from anthropic.types import ToolParam, TextBlockParam
import os
import requests
from datetime import datetime

# Existing types

type ExecutableActionResponse = Union[str, list[TextBlockParam]]
type ExecutableAction = Callable[..., ExecutableActionResponse]


class Actions:
    """Handles the registration and execution of actions."""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Actions, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "action_registry"):
            self.action_registry: dict[str, Callable] = {
                cast(ToolParam, item.__action__)['name']: cast(ExecutableAction, item)
                for item in Actions.__dict__.values()
                if hasattr(item, "__action__")
            }

            self.action_schemas = [
                cast(ToolParam, item.__action__)
                for item in Actions.__dict__.values()
                if hasattr(item, "__action__")
            ]

    def execute(self, action_identifier: str, action_input: dict) -> str:
        """Executes the action with the given name and input."""
        if action_identifier not in self.action_registry:
            raise ValueError(f"Action {action_identifier} not found.")
        action = self.action_registry[action_identifier]
        return action(self, **action_input)

    # ------------------------------ get_weather ------------------------------ #

    def get_weather(self, location: str) -> ExecutableActionResponse:
        """
        Fetches current weather and daily forecast for the provided city.
        """
        api_key = os.environ.get("OPEN_WEATHER_API_KEY")
        if not api_key:
            raise ValueError("API key for OpenWeatherMap is not set.")

        lat, lon = self._geocode(location)

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
        current = data.get("current", {})
        temp = current.get("temp")
        weather = current.get("weather", [])
        desc = weather[0].get("description") if weather else "no description"

        daily = data.get("daily", [])
        if daily:
            today = daily[0].get("temp", {})
            min_temp = today.get("min")
            max_temp = today.get("max")
            return [TextBlockParam(type="text", text=(
                f"{location.title()}: {desc}, {temp:.1f}°F (min {min_temp:.1f}°F, max {max_temp:.1f}°F)"
            ))]
        else:
            return [TextBlockParam(type="text", text=(
                f"{location.title()}: {desc}, {temp:.1f}°F"
            ))]

    get_weather.__action__ = ToolParam(
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

    # ------------------------------ get_time ------------------------------ #

    def get_time(self) -> ExecutableActionResponse:
        now = datetime.now()
        return [TextBlockParam(type="text", text=now.strftime("%H:%M:%S"))]

    get_time.__action__ = ToolParam(
        name="get_time",
        description="Retrieves the current local time in HH:MM:SS format.",
        input_schema={
            "type": "object",
            "properties": {},
            "required": []
        }
    )

    # ------------------------------ get_date ------------------------------ #

    def get_date(self) -> ExecutableActionResponse:
        today = datetime.now()
        return [TextBlockParam(type="text", text=today.strftime("%Y-%m-%d"))]

    get_date.__action__ = ToolParam(
        name="get_date",
        description="Retrieves the current local date in YYYY-MM-DD format.",
        input_schema={
            "type": "object",
            "properties": {},
            "required": []
        }
    )
    # ------------------------------ get_stock_info ------------------------------ #

    def get_stock_info(self, tickers: list[str]) -> dict:
        """
        Retrieves current stock prices and related financial data for a list of provided stock tickers.
        """
        api_key = os.getenv("MARKET_STACK_API_KEY")
        if not api_key:
            raise ValueError("API key for MarketStack is not set.")

        url = "http://api.marketstack.com/v2/eod" + "?access_key=" + api_key + "&symbols="
        url += ",".join(tickers)
        url += "&limit=1"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            raise ValueError(f"Network error fetching stock data: {e}")

        data = response.json()
        return data

    get_stock_info.__action__ = ToolParam(
        name="get_stock_info",
        description=(
            "Retrieves current stock prices and related financial data for a list of provided stock tickers. "
            "Use when a user provides one or more stock symbols (e.g., ['AAPL', 'GOOG']). "
            "This tool fetches live stock market information and summarizes it for quick reference. "
            "Ticker symbols must be accurate as the tool does not auto-correct invalid inputs."
        ),
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

        # ------------------------------ get_crypto_price ------------------------------ #

    def get_crypto_price(self, coin: str, currency: str) -> dict:
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

    get_crypto_price.__action__ = ToolParam(
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


    # ------------------------------ _geocode ------------------------------ #

    def _geocode(self, city: str) -> Tuple[float, float]:
        """
        Helper: Convert a city name into (lat, lon) via OpenStreetMap Nominatim.
        """
        url = "https://nominatim.openstreetmap.org/search"
        params = {"q": city, "format": "json", "limit": 1}
        headers = {"User-Agent": "claude-tools/1.0"}

        try:
            resp = requests.get(url, params=params, headers=headers, timeout=5)
            resp.raise_for_status()
        except requests.RequestException as e:
            raise ValueError(f"Network error during geocoding: {e}")

        results = resp.json()
        if not results:
            raise ValueError(f"Could not geocode city '{city}'")

        lat = float(results[0]["lat"])
        lon = float(results[0]["lon"])
        return lat, lon