from elevenlabs import ElevenLabs
import os
from io import BytesIO
from vosk import Model
from vosk import KaldiRecognizer
import wave
import json
from globals import constants

model = Model(constants.vosk_model_path)

def audio_to_text(audio_fp: str) -> str:
    """Take an audio file path and return the transcribed text using vosk."""

    wf = wave.open(audio_fp, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        raise ValueError("Audio file must be WAV format mono PCM.")

    rec = KaldiRecognizer(model, wf.getframerate())
    results = []

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            results.append(res.get('text', ''))

    final_res = json.loads(rec.FinalResult())
    results.append(final_res.get('text', ''))

    return ' '.join(results)

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