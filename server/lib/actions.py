from typing import cast, Callable, Union
from anthropic.types import ToolParam, TextBlockParam

type ExecutableActionResponse = Union[str, list[TextBlockParam]]
type ExecutableAction = Callable[...,ExecutableActionResponse]

class Actions:
    """Handles the registration and execution of actions."""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Actions, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "action_registry"):
            # register all actions dynamically
            self.action_registry: dict[str, Callable] = {
                cast(ToolParam, item.__action__)['name']: cast(ExecutableAction, item) for item in Actions.__dict__.values() if hasattr(item, "__action__")
            }
            
            # register the actions schemas for claude
            self.action_schemas = [cast(ToolParam, item.__action__) for item in Actions.__dict__.values() if hasattr(item, "__action__")]

    def execute(self, action_identifier: str, action_input: dict) -> str:
        """Executes the action with the given name and input."""
        if action_identifier not in self.action_registry:
            raise ValueError(f"Action {action_identifier} not found.")
        action = self.action_registry[action_identifier]
        return action(self, **action_input)
    
    # -------------------------------- get weather ------------------------------- #
    
    def get_weather(self, location: str) -> ExecutableActionResponse:
        # api_key = os.environ.get("OPEN_WEATHER_API_KEY")
        # if not api_key:
        #     raise ValueError("API key for OpenWeatherMap is not set.")
        # url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=imperial"
        # response = requests.get(url)
        # data = response.json()
        # temp_f = data["main"]["temp"]
        # condition = data["weather"][0]["description"]
        # return TextBlockParam(type="text", text=f"The current temperature in {location} is {temp_f}°F with {condition}.")
        return [TextBlockParam(type="text", text=f"76°F with clear skies.")]
        # return f"The current temperature in {location} is 75°F with clear skies."
    
    get_weather.__action__ = ToolParam(
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