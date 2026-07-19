from flask import Blueprint, render_template, request, jsonify, send_from_directory, current_app
import os

from controller.image_controller import process_image, allowed_file, get_all_records

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in request'}), 400
    file = request.files['file']
    if not file or file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    if not allowed_file(file.filename):
        return jsonify({'error': 'Unsupported file type. Use JPG, PNG, BMP, TIFF, or WebP.'}), 415
    try:
        result = process_image(file)
        return jsonify(result), 200
    except Exception as exc:
        current_app.logger.exception('Image processing failed')
        return jsonify({'error': str(exc)}), 500


@bp.route('/history')
def history():
    return jsonify(get_all_records())


@bp.route('/uploads/<path:filename>')
def serve_upload(filename):
    upload_dir = os.path.join(current_app.root_path, 'uploads')
    return send_from_directory(upload_dir, filename)
