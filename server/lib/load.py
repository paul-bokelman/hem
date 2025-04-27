from dotenv import load_dotenv
import os
import urllib.request
import zipfile
from vosk import Model
from globals import constants

def preflight():
    vars = [
        "ANTHROPIC_API_KEY",
        "ADMIN_API_KEY",
        "OPEN_WEATHER_API_KEY",
        "ELEVEN_LABS_API_KEY",
        "APLHA_VANTAGE_KEY",
        "MARKET_STACK_API_KEY",
    ]

    """Check for missing environment variables."""
    load_dotenv()

    missing_env_vars: list[str] = []

    for var in vars:
        if os.getenv(var) is None:
            missing_env_vars.append(var)

    if len(missing_env_vars) > 0:
        print(f"Missing environment variables: {', '.join(missing_env_vars)}")
        exit(1)

def load_vosk_model():
    """Load the Vosk model if it exists."""

    if not os.path.exists(constants.vosk_model_path):
        print(f"Vosk model not found at {constants.vosk_model_path}. Downloading...")
        os.makedirs(constants.vosk_model_path, exist_ok=True)
        url = "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
        model_zip_path = "/tmp/vosk-model.zip"
        urllib.request.urlretrieve(url, model_zip_path)
        
        with zipfile.ZipFile(model_zip_path, 'r') as zip_ref:
            zip_ref.extractall(os.path.dirname(constants.vosk_model_path))

        
