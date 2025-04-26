import os
import io
from flask import Blueprint, request, jsonify, send_file
from services.utils import get_user_from_header
from lib import processor, conversions
import tempfile

pipeline_bp = Blueprint('pipeline', __name__)

processor_singleton = processor.Processor() # initialize the Processor class (singleton)

@pipeline_bp.route('/respond', methods=['POST'])
def response_pipeline():
    user = get_user_from_header()

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

    # transcribe and remove temp audio file
    try:
        transcription = conversions.audio_to_text(temp_file_path)
    finally:
        os.remove(temp_file_path)

    # ------------------------- process message with llm ------------------------- #

    response, actions_performed = processor_singleton.handle_message(user, transcription)

    # -------------------- convert back to audio and send back ------------------- #

    buffer = conversions.text_to_audio(response)

    return send_file(
        io.BytesIO(buffer.getvalue()),  # make sure it's a real BytesIO
        mimetype="audio/wav",
        as_attachment=False,
        download_name="response.wav"
    )

