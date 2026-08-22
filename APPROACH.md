# Approach (Write-up)

I built the Social Media Content Analyzer as a lightweight Flask app to keep the codebase easy to read and deploy within the given time budget.

For **document upload**, the frontend uses native drag-and-drop events plus a file-picker fallback, sending files to the backend via `multipart/form-data` — no heavy JS framework needed.

For **text extraction**, I split logic by file type: PDFs go through `pdfplumber`, which reads page-by-page and keeps line breaks reasonably close to the original layout; images go through `Tesseract OCR` via `pytesseract`, chosen because it's free, open-source, and doesn't require an external API key or paid tier.

For **engagement insights**, rather than calling a paid ML/sentiment API, I implemented simple, transparent rule-based heuristics (word count, hashtag/mention/link detection, average sentence length) that produce actionable, explainable suggestions — e.g., flagging posts with no hashtags or overly long sentences.

**Error handling** covers unsupported file types, empty extraction results, and processing failures, each surfaced clearly in the UI. A loading spinner covers the extraction wait time.

The app is packaged with a Dockerfile (installing the Tesseract binary) so it deploys reliably to any container-based free host without manual system configuration.
