"""EasyOCR wrapper — lazily initialises the reader on first call.

Improvements over v1
--------------------
* Image pre-processing (contrast + sharpness enhancement, normalisation) via
  Pillow so that faint, low-contrast or small text is more reliably detected.
* ``detail=1`` + explicit confidence filtering (threshold 0.25) instead of the
  opaque ``paragraph=True`` merge which silently discards weak detections.
* Reading order reconstruction: detections are sorted top-to-bottom then
  left-to-right so the returned string reflects the visual layout.
* ``verbose=False`` keeps the EasyOCR reader silent (no more console chatter).
* EasyOCR ``readtext`` knobs:
    - ``text_threshold=0.5``  (default 0.7) — accept lower-confidence glyphs
    - ``low_text=0.3``        (default 0.4) — catch small / faint characters
    - ``contrast_ths=0.1``    (default 0.1) — auto-contrast for dark images
    - ``adjust_contrast=0.7`` (default 0.5) — stronger contrast boost
    - ``decoder='beamsearch'`` + ``beamWidth=10`` — more accurate decoding
    - ``mag_ratio=1.5``       — up-scale the image before detection
"""
import io

import easyocr
from PIL import Image, ImageEnhance, ImageFilter

_reader = None

# Minimum confidence to keep a detected text span (0–1).
_CONFIDENCE_THRESHOLD = 0.25


def _get_reader() -> easyocr.Reader:
    global _reader
    if _reader is None:
        _reader = easyocr.Reader(
            ['en'],
            gpu=False,
            verbose=False,   # suppress EasyOCR's own progress output
        )
    return _reader


def _preprocess(image_path: str) -> str:
    """Return a pre-processed copy of the image as a temp file path.

    Steps applied:
    1. Convert to RGB (handles RGBA PNGs, palette-mode GIFs, etc.)
    2. Upscale very small images so EasyOCR can locate characters reliably.
    3. Boost contrast and sharpness to surface faint ink/pixels.
    4. Light unsharp-mask to crisp up edges.
    """
    img = Image.open(image_path).convert('RGB')

    # --- upscale if either dimension is below 600 px ---
    w, h = img.size
    min_dim = min(w, h)
    if min_dim < 600:
        scale = max(2, 600 // min_dim)
        img = img.resize((w * scale, h * scale), Image.LANCZOS)

    # --- contrast ---
    img = ImageEnhance.Contrast(img).enhance(1.8)

    # --- sharpness ---
    img = ImageEnhance.Sharpness(img).enhance(2.0)

    # --- mild unsharp mask ---
    img = img.filter(ImageFilter.UnsharpMask(radius=1, percent=120, threshold=3))

    # Save to an in-memory buffer; easyocr can accept a bytes object.
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()   # raw PNG bytes


def _sort_key(detection):
    """Sort detections top-to-bottom, then left-to-right.

    ``detection`` is ``(bbox, text, confidence)`` where bbox is four
    ``[x, y]`` corner points starting from the top-left.
    """
    bbox = detection[0]
    top  = min(pt[1] for pt in bbox)
    left = min(pt[0] for pt in bbox)
    # Bucket rows into bands of ~20 px so slight vertical jitter doesn't
    # break the left-to-right ordering within a single text line.
    return (round(top / 20), left)


def extract_text_from_image(image_path: str) -> str:
    """Run EasyOCR on *image_path* and return extracted text.

    Returns a single string with detections separated by newlines,
    ordered by their visual position in the image.
    """
    reader     = _get_reader()
    img_bytes  = _preprocess(image_path)

    results = reader.readtext(
        img_bytes,
        detail=1,              # get (bbox, text, confidence) tuples
        paragraph=False,       # keep individual detections; we reconstruct order
        text_threshold=0.5,    # lower than default 0.7 → catch more glyphs
        low_text=0.3,          # lower than default 0.4 → catch small characters
        contrast_ths=0.1,
        adjust_contrast=0.7,   # stronger auto-contrast inside EasyOCR
        decoder='beamsearch',  # better accuracy than 'greedy'
        beamWidth=10,
        mag_ratio=1.5,         # internally up-scale before detection
    )

    # Filter by confidence, then sort into reading order.
    filtered = [r for r in results if r[2] >= _CONFIDENCE_THRESHOLD]
    filtered.sort(key=_sort_key)

    return '\n'.join(text for _, text, _ in filtered)
