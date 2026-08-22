"""
Social Media Content Analyzer
------------------------------
Flask backend that accepts PDF or image uploads, extracts text
(via pdfplumber for PDFs and Tesseract OCR for images), and returns
the extracted text along with lightweight content-engagement insights.
"""

import os
import re
import io
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import pdfplumber
from PIL import Image
import pytesseract

app = Flask(__name__)

ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg", "webp", "bmp", "tiff"}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_pdf(file_stream) -> str:
    """Extract text from a PDF, page by page, preserving basic layout via newlines."""
    text_parts = []
    with pdfplumber.open(file_stream) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            page_text = page.extract_text() or ""
            if page_text.strip():
                text_parts.append(f"--- Page {i} ---\n{page_text.strip()}")
    return "\n\n".join(text_parts).strip()


def extract_text_from_image(file_stream) -> str:
    """Run OCR on an image using Tesseract."""
    image = Image.open(file_stream)
    if image.mode != "RGB":
        image = image.convert("RGB")
    text = pytesseract.image_to_string(image)
    return text.strip()


PLATFORM_RULES = {
    "instagram": {"char_limit": 2200, "ideal_hashtags": (5, 15), "label": "Instagram"},
    "twitter": {"char_limit": 280, "ideal_hashtags": (1, 3), "label": "Twitter / X"},
    "linkedin": {"char_limit": 3000, "ideal_hashtags": (3, 5), "label": "LinkedIn"},
    "general": {"char_limit": None, "ideal_hashtags": (2, 8), "label": "General"},
}

EMOJI_PATTERN = re.compile(
    "["
    "\U0001F300-\U0001FAFF"
    "\U00002600-\U000027BF"
    "\U0001F1E6-\U0001F1FF"
    "]+",
    flags=re.UNICODE,
)


def estimate_reading_time(word_count: int) -> str:
    """Rough reading time at ~200 wpm, floored at a few seconds for tiny posts."""
    minutes = word_count / 200
    if minutes < 0.17:  # under ~10 seconds
        return "a few seconds"
    if minutes < 1:
        return f"~{max(1, round(minutes * 60))} sec"
    return f"~{round(minutes, 1)} min"


def analyze_content(text: str, platform: str = "general") -> dict:
    """Rule-based content/engagement analysis, tuned per platform."""
    rules = PLATFORM_RULES.get(platform, PLATFORM_RULES["general"])

    words = re.findall(r"\b\w+\b", text)
    word_count = len(words)
    char_count = len(text)
    hashtags = re.findall(r"#\w+", text)
    mentions = re.findall(r"@\w+", text)
    urls = re.findall(r"https?://\S+", text)
    emojis = EMOJI_PATTERN.findall(text)
    emoji_count = sum(len(e) for e in emojis)
    sentences = [s for s in re.split(r"[.!?]+", text) if s.strip()]
    avg_sentence_len = round(word_count / len(sentences), 1) if sentences else 0
    reading_time = estimate_reading_time(word_count)

    min_tags, max_tags = rules["ideal_hashtags"]

    suggestions = []
    if len(hashtags) == 0:
        suggestions.append(f"Consider adding {min_tags}-{max_tags} relevant hashtags — ideal range for {rules['label']}.")
    elif len(hashtags) > max_tags:
        suggestions.append(f"You're using more hashtags than typical for {rules['label']} — consider trimming to {min_tags}-{max_tags}.")
    elif len(hashtags) < min_tags:
        suggestions.append(f"A few more hashtags (aim for {min_tags}-{max_tags}) could help on {rules['label']}.")

    if rules["char_limit"] and char_count > rules["char_limit"]:
        suggestions.append(f"This post is over {rules['label']}'s typical {rules['char_limit']}-character comfort zone by {char_count - rules['char_limit']} characters.")

    if word_count > 0 and word_count < 8:
        suggestions.append("The post is very short — consider adding more context or a call-to-action.")

    if len(urls) == 0 and word_count > 15:
        suggestions.append("Adding a relevant link could help drive traffic if that's your goal.")

    if avg_sentence_len > 25:
        suggestions.append("Sentences are quite long on average — shorter sentences tend to read better on social media.")

    if emoji_count == 0 and platform in ("instagram", "twitter"):
        suggestions.append("A well-placed emoji or two can boost visual engagement on this platform.")

    if not any(ch in text for ch in "!?"):
        suggestions.append("Consider adding a question or exclamation to encourage engagement.")

    if not suggestions:
        suggestions.append("Content looks well-balanced for this platform. No major issues detected.")

    return {
        "word_count": word_count,
        "character_count": char_count,
        "hashtag_count": len(hashtags),
        "hashtags": hashtags,
        "mention_count": len(mentions),
        "mentions": mentions,
        "url_count": len(urls),
        "emoji_count": emoji_count,
        "avg_sentence_length": avg_sentence_len,
        "reading_time": reading_time,
        "platform": rules["label"],
        "suggestions": suggestions,
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/analyze", methods=["POST"])
def analyze():
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request."}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected."}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Unsupported file type. Please upload a PDF or image (png/jpg/jpeg/webp/bmp/tiff)."}), 400

    platform = request.form.get("platform", "general")
    if platform not in PLATFORM_RULES:
        platform = "general"

    filename = secure_filename(file.filename)
    ext = filename.rsplit(".", 1)[1].lower()
    file_bytes = file.read()

    try:
        if ext == "pdf":
            text = extract_text_from_pdf(io.BytesIO(file_bytes))
            source_type = "pdf"
        else:
            text = extract_text_from_image(io.BytesIO(file_bytes))
            source_type = "image"
    except Exception as e:
        return jsonify({"error": f"Failed to process file: {str(e)}"}), 500

    if not text:
        return jsonify({
            "filename": filename,
            "source_type": source_type,
            "extracted_text": "",
            "analysis": None,
            "warning": "No text could be extracted from this file."
        }), 200

    analysis = analyze_content(text, platform)

    return jsonify({
        "filename": filename,
        "source_type": source_type,
        "extracted_text": text,
        "analysis": analysis,
    }), 200


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
