import pyaudio
from anthropic.types import ModelParam

# ---------------------------------- general --------------------------------- #

preferred_input = None # 'text', 'audio', 'None

# ------------------------------------ ai ------------------------------------ #

# -------------------------------- inquisitive ------------------------------- #
include_context = False # include context in subsequent 'inquisitive' questions (!unused!)
concise_questions = True # whether or not responses should be short and sweet
max_questions = 1 # maximum number of questions to ask per message (inquisitive mode)
inquisitive_max_tokens = 1024 # maximum number of tokens to generate
inquisitive_max_audio_length = 1000 * 60 * 5 # maximum length of audio recording (inquisitive mode) (5 minutes)
inquisitive_model: ModelParam = 'claude-3-haiku-20240307' # model to use for inquisitive mode (note: different models require different max tokens)

# -------------------------------- compilation ------------------------------- #
compilation_max_tokens = 8192 # maximum number of tokens to generate (compilation mode)
compilation_template = 'basic-notes.md' # template under /templates or None
compilation_max_audio_length = None # maximum length of audio recording (compilation mode) (defaults to 30m)
compilation_output_path = 'notes' # output path for compilation mode
compilation_model: ModelParam = 'claude-3-5-sonnet-latest' # model to use for compilation mode (note: different models require different max tokens)

# ---------------------------------- audio ---------------------------------- #
temp_audio_out = "output.wav"
FORMAT = pyaudio.paInt16 # audio format (16-bit)
CHANNELS = 1 # number of audio channels (mono)
RATE = 44100 # sampling rate (44.1 kHz)
CHUNK = 1024 # buffer size
RECORD_SECONDS = 3 # duration of recording'
default_max_audio_length = 1000 * 60 * 30 # 30 minutes