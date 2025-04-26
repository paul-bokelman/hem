from gtts import gTTS
import requests
from elevenlabs import ElevenLabs
from dotenv import load_dotenv
import os

load_dotenv()

def tts_mp3(text_to_convert : str) -> str:
    """Takes an input string and uses Eleven Labs API to generate speech and save it as an MP3 file.
    Returns the name of the new MP3."""
    
    client = ElevenLabs(
        api_key=os.getenv("ELEVEN_LABS_API_KEY")
    )

    response = client.text_to_speech.convert(
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        output_format="mp3_44100_128",
        text=text_to_convert,
        model_id="eleven_multilingual_v2",
    )

    filename = "tts_output.mp3"
    with open(filename, 'wb') as f:
            for chunk in response:  # response is a generator
                f.write(chunk)

    return filename

