from typing import Optional, Union, cast
from whisper import Whisper
import os
import sys
import contextlib
from termcolor import colored
import inquirer
import whisper
import pyaudio
from pynput import keyboard as pynput_keyboard
import wave
import constants

model = whisper.load_model("base")

def transcribe(audio_fp : str) -> str:
    """Takes a fp to an mp3, transcribes the mp3, then returns the transcription of it as a string."""
    audio =  whisper.load_audio(audio_fp)
    audio = whisper.pad_or_trim(audio)
    transcription = model.transcribe(audio)
    stripped = transcription["text"].strip()
    with open("transcription.txt", "w") as file:
        file.write(stripped)
    return stripped
