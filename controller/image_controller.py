"""Image upload controller: saves file, persists to DB, runs OCR."""
import os
from flask import current_app
from werkzeug.utils import secure_filename

from extensions import db
from model.image_model import Image
from model.text_to_image_model import TextToImage
from service.ocr_service import extract_text_from_image

ALLOWED_EXT = {'png', 'jpg', 'jpeg', 'bmp', 'tiff', 'tif', 'webp', 'gif'}
UPLOAD_FOLDER = 'uploads'


def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT


def process_image(file) -> dict:
    """
    1. Save uploaded file to disk.
    2. Insert an Image record (stores the URL/path).
    3. Run EasyOCR and insert a TextToImage record.
    Returns a dict with image metadata and extracted text.
    """
    filename   = secure_filename(file.filename)
    upload_dir = os.path.join(current_app.root_path, UPLOAD_FOLDER)
    os.makedirs(upload_dir, exist_ok=True)

    filepath = os.path.join(upload_dir, filename)
    file.save(filepath)

    # ── persist image record ──
    image_url    = f'/uploads/{filename}'
    image_record = Image(image_url=image_url)
    db.session.add(image_record)
    db.session.flush()          # get auto-generated id before FK insert

    # ── extract text ──
    extracted_text = extract_text_from_image(filepath)

    # ── persist text record ──
    text_record = TextToImage(image_id=image_record.id, text=extracted_text)
    db.session.add(text_record)
    db.session.commit()

    return {
        'image_id':  image_record.id,
        'image_url': image_url,
        'filename':  filename,
        'text':      extracted_text,
    }


def get_all_records() -> list:
    """Return all text-to-image records joined with their image data, newest first."""
    rows = (
        db.session.query(TextToImage, Image)
        .join(Image, TextToImage.image_id == Image.id)
        .order_by(TextToImage.id.desc())
        .all()
    )
    return [
        {
            'id':        tti.id,
            'image_id':  img.id,
            'image_url': img.image_url,
            'filename':  img.image_url.rsplit('/', 1)[-1],
            'text':      tti.text,
        }
        for tti, img in rows
    ]
