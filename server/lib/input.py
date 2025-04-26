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

class Input:
    """Prompt and process audio or text input from the user."""
    def __init__(self) -> None:
        self.model = None

        # only load the model if the preferred input is audio or indifferent
        if constants.preferred_input is None or constants.preferred_input == "audio":
            print(colored("Loading audio transcription model...", "dark_grey"))
            with open(os.devnull, 'w') as f, contextlib.redirect_stdout(f), contextlib.redirect_stderr(f):
                self.model: Union[Whisper, None] = whisper.load_model("base")
            print(f"{colored('Model loaded.', 'green')}\n")

    def _record_and_transcribe(self, max_length = constants.default_max_audio_length) -> str:
        audio = pyaudio.PyAudio()

        stream = audio.open(format=constants.FORMAT, channels=constants.CHANNELS,
                            rate=constants.RATE, input=True,
                            frames_per_buffer=constants.CHUNK)

        frames = []
        stop_recording = False

        def on_press(key) -> None:
            nonlocal stop_recording
            try:
                if key.char == 'q':
                    stop_recording = True
            except AttributeError:
                pass

        listener = pynput_keyboard.Listener(on_press=on_press)
        listener.start()

        print("Recording... Press 'q' to stop.")

        # continue recording until the user stops or the max length is reached
        while not stop_recording and len(frames) < max_length * constants.RATE / constants.CHUNK:
            data = stream.read(constants.CHUNK)
            frames.append(data)

        listener.stop()
        stream.stop_stream()
        stream.close()
        audio.terminate()

        sys.stdout.write("\r") # Cursor up one line
        print(colored("Recording stopped, processing...", "dark_grey"))

        # save recorded audio to a temporary file
        with wave.open(constants.temp_audio_out, 'wb') as wf:
            wf.setnchannels(constants.CHANNELS)
            wf.setsampwidth(audio.get_sample_size(constants.FORMAT))
            wf.setframerate(constants.RATE)
            wf.writeframes(b''.join(frames))

        assert self.model is not None, "Model not loaded"

        # transcribe and remove temporary audio file
        transcription = self.model.transcribe(constants.temp_audio_out)
        os.remove(constants.temp_audio_out)

        return cast(str, transcription["text"]).strip()

    def get_input(self, input_type: Optional[str] = None, max_audio_length: Optional[int] = None) -> tuple[str, str]:
        """Get audio or text input from the user, depending on prompt response and preferred input."""

        if constants.preferred_input is None and input_type is None:
            input_type_question = [inquirer.List('input_type', message="Choose input format", choices=["audio", "text"])]
            input_type_answers = inquirer.prompt(input_type_question, raise_keyboard_interrupt=True)
            assert input_type_answers is not None, "Input_type selection is required"
            input_type = input_type_answers["input_type"]
        else:
            input_type = constants.preferred_input if constants.preferred_input is not None else input_type

        if input_type not in ["audio", "text"]:
            raise ValueError("Invalid input_type. Must be 'audio' or 'text'.")

        # wants text -> prompt and return text response
        if input_type == "text" or constants.preferred_input == "text":
            
            # get text and color the users input
            text = input(colored("You", "green") + ": ")

            assert len(text) != 0, "Empty text input"
            return text, input_type
        
        # wants audio -> record, process, and transcribe audio response
        with open(os.devnull, 'w') as f, contextlib.redirect_stderr(f):
            start_recording_question = [inquirer.Confirm('start_recording', message="Start recording?")]
            start_recording_answers = inquirer.prompt(start_recording_question, raise_keyboard_interrupt=True)
            assert start_recording_answers is not None, "'Start recording' selection is required"
            start_recording = start_recording_answers["start_recording"]

            # ensure the user wants to start recording
            if start_recording:
                response = self._record_and_transcribe(max_audio_length if max_audio_length is not None else constants.default_max_audio_length)
            else:
                raise KeyboardInterrupt

            print(f"\n{colored('You', 'green')}: {response}\n")

            return response, input_type