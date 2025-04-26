from typing import cast
from elevenlabs import ElevenLabs
import os

import whisper
from io import BytesIO

model = whisper.load_model("base")

def audio_to_text(audio_fp: str) -> str:
    """Take an audio file path and return the transcribed text using openai/whisper."""
    audio = whisper.load_audio(audio_fp)
    audio = whisper.pad_or_trim(audio)
    transcription = model.transcribe(audio)
    return cast(str, transcription["text"]).strip()

def text_to_audio(text : str) -> BytesIO:
    """Takes an input string and uses Eleven Labs API to generate speech and save it as an MP3 file.
    Returns the name of the new MP3."""

    client = ElevenLabs(
        api_key=os.getenv("ELEVEN_LABS_API_KEY")
    )

    response = client.text_to_speech.convert(
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        output_format="mp3_44100_128",
        text=text,
        model_id="eleven_multilingual_v2",
    )

    audio_buffer = BytesIO()
    for chunk in response:  # response is a generator
        audio_buffer.write(chunk)

    audio_buffer.seek(0)  # reset buffer pointer to the beginning
    return audio_buffer