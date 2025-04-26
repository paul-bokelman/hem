# tools-form.py
tools = [
    {
        "name": "get_weather",
        "description": (
            "Retrieves the current weather for a specified location..."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, like 'Austin, TX'."
                }
            },
            "required": ["location"]
        }
    }
]
