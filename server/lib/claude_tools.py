# claude_tools.py

import os
import requests

def tool(name: str, description: str, input_schema: dict):
    def decorator(func):
        func.__tool__ = {
            "name": name,
            "description": description,
            "input_schema": input_schema
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
def get_weather(location: str) -> str:
    api_key = os.environ.get("OPEN_WEATHER_API_KEY")
    if not api_key:
        raise ValueError("API key for OpenWeatherMap is not set.")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=imperial"
    response = requests.get(url)
    data = response.json()
    temp_f = data["main"]["temp"]
    condition = data["weather"][0]["description"]
    return f"{temp_f}°F and {condition}."

