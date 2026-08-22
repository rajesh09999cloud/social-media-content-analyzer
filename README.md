
## Running Locally

### Prerequisites
- Python 3.10+
- Tesseract OCR installed on your system:
  - macOS: `brew install tesseract`
  - Ubuntu/Debian: `sudo apt-get install tesseract-ocr`
  - Windows: [Tesseract installer](https://github.com/UB-Mannheim/tesseract/wiki)

### Steps
```bash
git clone https://github.com/rajesh09999cloud/social-media-content-analyzer.git
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
- Body: `multipart/form-data` with:
  - `file` — the PDF or image to analyze
  - `platform` (optional) — one of `general`, `instagram`, `twitter`, `linkedin`. Defaults to `general`.
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
    "emoji_count": 0,
    "avg_sentence_length": 4.8,
    "reading_time": "a few seconds",
    "platform": "General",
    "suggestions": ["..."]
  }
}
```

## Deployment

The app is packaged with a `Dockerfile` (installing the Tesseract binary at build time) so it deploys reliably to any container-based host without manual system configuration. Currently deployed on **Render** (free tier, Docker environment).

## Notes

- Max upload size: 16MB
- OCR accuracy depends on image quality; clean, high-contrast scans/screenshots work best
- The engagement analysis is intentionally simple and rule-based (word/hashtag/link heuristics) rather than ML-based, to keep the app fast, dependency-light, and easy to reason about

## Author

**Rajesh Vinjam**
- GitHub: [github.com/rajesh09999cloud](https://github.com/rajesh09999cloud?tab=repositories)
- LinkedIn: [linkedin.com/in/rajesh-vinjam-5a2261320](https://www.linkedin.com/in/rajesh-vinjam-5a2261320)
