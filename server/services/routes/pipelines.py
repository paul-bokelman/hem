import os
import io
from flask import Blueprint, request, jsonify, send_file
from services.utils import get_user_from_header
from lib import processor, conversions
import pydub
import tempfile

pipeline_bp = Blueprint('pipeline', __name__)

processor_singleton = processor.Processor() # initialize the Processor class (singleton)

@pipeline_bp.route('/respond', methods=['POST'])
def response_pipeline():
    user_id = get_user_from_header()

    # ----------------------------- transcribe audio ----------------------------- #

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # save the file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        file.save(tmp.name)
        tmp.flush()
        temp_file_path = tmp.name

    # convert the audio to WAV format, mono channel, PCM encoding
    audio = pydub.AudioSegment.from_file(temp_file_path)
    audio = audio.set_channels(1)  # convert to mono
    audio = audio.set_frame_rate(16000)  # set sample rate to 16 kHz
    audio = audio.set_sample_width(2)  # set sample width to 16-bit (PCM)
    wav_path = temp_file_path + ".wav"
    audio.export(wav_path, format="wav", codec="pcm_s16le")  # export as PCM WAV

    try:
        transcription = conversions.audio_to_text(wav_path)
    finally:
        os.remove(temp_file_path)
        os.remove(wav_path)

    # ------------------------- process message with llm ------------------------- #

    response, actions_performed = processor_singleton.handle_message(user_id, transcription)

    # -------------------- convert back to audio and send back ------------------- #

    buffer = conversions.text_to_audio(response)

    return send_file(
        io.BytesIO(buffer.getvalue()),  # make sure it's a real BytesIO
        mimetype="audio/wav",
        as_attachment=False,
        download_name="response.wav"
    )