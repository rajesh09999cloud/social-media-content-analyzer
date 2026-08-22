# Social Media Content Analyzer

A web application that extracts text from social media post files (PDFs or images) and provides quick, rule-based engagement suggestions.

## Features

- **Document Upload** — drag-and-drop or file-picker upload for PDFs and images (PNG, JPG, JPEG, WEBP, BMP, TIFF)
- **PDF Text Extraction** — extracts text page-by-page using `pdfplumber`, preserving basic layout
- **OCR for Images** — extracts text from scanned/image posts using `Tesseract OCR` via `pytesseract`
- **Platform-aware analysis** — pick General, Instagram, Twitter/X, or LinkedIn, and suggestions adapt to that platform's character limits and typical hashtag ranges
- **Content Insights** — word/character/emoji counts, hashtag & mention detection, link count, average sentence length, estimated reading time, and rule-based engagement suggestions
- **Copy & export** — one-click copy of extracted text, and a downloadable `.txt` report of the full analysis
- **UX** — loading spinner during processing, clear error messages for unsupported files or extraction failures

## Tech Stack

- **Backend**: Python, Flask
- **PDF parsing**: pdfplumber
- **OCR**: Tesseract OCR (via pytesseract) + Pillow
- **Frontend**: Vanilla HTML/CSS/JS (no framework, keeps it lightweight)
- **Server**: Gunicorn (production), Flask dev server (local)

## Project Structure

```
social-media-content-analyzer/
├── app.py                 # Flask backend (routes, PDF/OCR extraction, analysis logic)
├── requirements.txt        # Python dependencies
├── Dockerfile               # Container definition (installs Tesseract + deps)
├── templates/
│   └── index.html          # Main page
├── static/
│   ├── style.css
│   └── script.js            # Upload handling, drag-and-drop, rendering
├── .gitignore
└── README.md
```

## Running Locally

### Prerequisites
- Python 3.10+
- Tesseract OCR installed on your system:
  - macOS: `brew install tesseract`
  - Ubuntu/Debian: `sudo apt-get install tesseract-ocr`
  - Windows: [Tesseract installer](https://github.com/UB-Mannheim/tesseract/wiki)

### Steps
```bash
git clone <your-repo-url>
cd social-media-content-analyzer
pip install -r requirements.txt
python app.py
```
Visit `http://localhost:5000`.

## Running with Docker (no local Tesseract install needed)

```bash
docker build -t content-analyzer .
docker run -p 5000:5000 content-analyzer
```
Visit `http://localhost:5000`.

## API

`POST /api/analyze`
- Body: `multipart/form-data` with a `file` field (PDF or image)
- Response:
```json
{
  "filename": "post.pdf",
  "source_type": "pdf",
  "extracted_text": "...",
  "analysis": {
    "word_count": 19,
    "character_count": 112,
    "hashtag_count": 2,
    "hashtags": ["#launch", "#excited"],
    "mention_count": 0,
    "mentions": [],
    "url_count": 1,
    "avg_sentence_length": 4.8,
    "suggestions": ["..."]
  }
}
```

## Notes

- Max upload size: 16MB
- OCR accuracy depends on image quality; clean, high-contrast scans work best
- The engagement analysis is intentionally simple and rule-based (word/hashtag/link heuristics) rather than ML-based, to keep the app fast, dependency-light, and easy to reason about within the project scope
