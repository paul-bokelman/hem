import os
from flask import Blueprint, request, abort, jsonify
from services.utils import get_user_from_header
from globals import constants

utilities_bp = Blueprint('macros', __name__)

@utilities_bp.route('/upload', methods=['POST'])
def upload_file():
    user = get_user_from_header()
    if 'file' not in request.files:
        abort(400, 'No file part')
    file = request.files['file']
    if file.filename == '':
        abort(400, 'No selected file')
    save_path = os.path.join(constants.upload_folder, f"{user.id}_{file.filename}")
    file.save(save_path)
    return jsonify({'filename': file.filename, 'path': save_path}), 201
