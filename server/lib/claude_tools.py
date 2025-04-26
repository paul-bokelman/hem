# claude_tools.py

import os
import requests
import inspect
from typing import Any, Callable, Dict, List
from dotenv import load_dotenv



class ClaudeTools:
    """
    Registry for Claude-compatible tools.
    """
load_dotenv()   # reads .env in cwd and updates os.environ

def __init__(self):
    # Discover methods decorated with __tool__ metadata
    self._tool_funcs: Dict[str, Callable[..., Any]] = {}
    for _, method in inspect.getmembers(self, predicate=inspect.ismethod):
        if hasattr(method, "__tool__"):
            meta = method.__tool__
            self._tool_funcs[meta["name"]] = method

    @staticmethod
    def tool(name: str, description: str, input_schema: dict):
        """
        Decorator to attach tool metadata to methods.
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
        name="get_weather",
        description="Retrieves the current weather for a given location.",
        input_schema={
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, like 'Austin, TX'."
                }
            },
            "required": ["location"]
        }
    )
    def get_weather(self, location: str) -> str:
        api_key = os.environ.get("OPEN_WEATHER_API_KEY")
        if not api_key:
            raise ValueError("API key for OpenWeatherMap is not set.")
        url = (
            f"http://api.openweathermap.org/data/2.5/weather"
            f"?q={location}&appid={api_key}&units=imperial"
        )
        data = requests.get(url).json()
        temp_f = data["main"]["temp"]
        condition = data["weather"][0]["description"]
        return f"{temp_f}°F and {condition}."

    def list_tools(self) -> List[dict]:
        """
        Return metadata for all registered tools. Pass into Claude as `tools=list_tools()`.
        """
        return [fn.__tool__ for fn in self._tool_funcs.values()]

    def run_tool(self, name: str, params: dict) -> Any:
        """
        Invoke the registered tool by name with given parameters.
        """
        if name not in self._tool_funcs:
            raise KeyError(f"Unknown tool: {name!r}")
        return self._tool_funcs[name](**params)
