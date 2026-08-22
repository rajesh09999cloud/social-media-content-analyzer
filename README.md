<div align="center">

# 📊 Social Media Content Analyzer

**Extract text from social media posts and get platform-aware engagement insights — instantly.**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Visit%20App-6C63FF?style=for-the-badge)](https://social-media-content-analyzer-dl6d.onrender.com/)
[![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-black?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

**[🚀 Live App](https://social-media-content-analyzer-dl6d.onrender.com/)** &nbsp;|&nbsp; **[📁 Repository](https://github.com/rajesh09999cloud/social-media-content-analyzer)**

</div>

---

> ⏳ **Note:** This app runs on Render's free tier, which spins down after periods of inactivity. If the link hasn't been visited recently, the first load may take 30–60 seconds while the server wakes up. This is expected behavior, not a bug.

---

## 📖 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Live Demo](#live-demo)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Run Locally](#run-locally)
  - [Run with Docker](#run-with-docker)
- [API Reference](#api-reference)
- [Deployment](#deployment)
- [Notes & Limitations](#notes--limitations)
- [Author](#author)

---

## Overview

**Social Media Content Analyzer** is a full-stack web application built to satisfy a technical assessment with three core requirements:

| # | Requirement | Implementation |
|---|---|---|
| 1 | **Document Upload** | Drag-and-drop or file-picker upload for PDFs and images |
| 2 | **Text Extraction** | PDF parsing (layout-aware) + OCR for scanned images |
| 3 | **Production-quality UX** | Loading states, error handling, clean architecture |

Beyond the base requirements, the app also analyzes extracted text and returns **platform-specific engagement suggestions** — tuned separately for Instagram, Twitter/X, and LinkedIn.

---

## ✨ Features

- 📤 **Document Upload** — drag-and-drop or file-picker upload for PDFs and images (PNG, JPG, JPEG, WEBP, BMP, TIFF)
- 📄 **PDF Text Extraction** — page-by-page extraction via `pdfplumber`, preserving basic layout
- 🔍 **OCR for Images** — text extraction from scanned/photographed posts using `Tesseract OCR`
- 🎯 **Platform-Aware Analysis** — General / Instagram / Twitter-X / LinkedIn modes, each with tuned character limits and hashtag guidance
- 📊 **Content Insights** — word count, character count, emoji count, hashtags, mentions, links, average sentence length, and estimated reading time
- 💡 **Smart Suggestions** — rule-based, explainable engagement tips (e.g. hashtag balance, post length, missing CTA)
- 📋 **Copy to Clipboard** — one-click copy of extracted text
- 📥 **Downloadable Report** — export the full analysis as a `.txt` file
- ⚡ **Polished UX** — loading spinner during processing, clear inline error messages for unsupported files or failed extraction

---

## 🌐 Live Demo

**[https://social-media-content-analyzer-dl6d.onrender.com/](https://social-media-content-analyzer-dl6d.onrender.com/)**

Try it with a PDF export of a post or a screenshot from Instagram, Twitter/X, or LinkedIn.

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| PDF Parsing | pdfplumber |
| OCR Engine | Tesseract OCR (via pytesseract) + Pillow |
| Frontend | Vanilla HTML, CSS, JavaScript |
| Production Server | Gunicorn |
| Containerization | Docker |
| Hosting | Render (free tier) |

social-media-content-analyzer/
├── app.py # Flask backend — routes, PDF/OCR extraction, analysis logic
├── requirements.txt # Python dependencies
├── Dockerfile # Container definition (installs Tesseract + deps)
├── templates/
│ └── index.html # Main page
├── static/
│ ├── style.css
│ └── script.js # Upload handling, drag-and-drop, results rendering
├── .gitignore
├── APPROACH.md # Written approach / design rationale
└── README.md
---

## 📂 Project Structure

---

## 🚀 Getting Started

### Run Locally

**Prerequisites:** Python 3.10+, and Tesseract OCR installed on your system.

| OS | Install Command |
|---|---|
| macOS | `brew install tesseract` |
| Ubuntu / Debian | `sudo apt-get install tesseract-ocr` |
| Windows | [Tesseract installer](https://github.com/UB-Mannheim/tesseract/wiki) |

```bash
git clone https://github.com/rajesh09999cloud/social-media-content-analyzer.git
cd social-media-content-analyzer
pip install -r requirements.txt
python app.py
```

Then open **http://localhost:5000**.

### Run with Docker

No local Tesseract install needed — the Dockerfile handles it.

```bash
docker build -t content-analyzer .
docker run -p 5000:5000 content-analyzer
```

Then open **http://localhost:5000**.

---

## 🔌 API Reference

### `POST /api/analyze`

Analyzes an uploaded file and returns extracted text plus content insights.

**Request:** `multipart/form-data`

| Field | Type | Required | Description |
|---|---|---|---|
| `file` | File | ✅ | PDF or image to analyze |
| `platform` | String | ❌ | `general` \| `instagram` \| `twitter` \| `linkedin` (defaults to `general`) |

**Response:**

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

---

## 🚢 Deployment

The app ships with a `Dockerfile` that installs the Tesseract binary at build time, so it deploys reliably to any container-based host without manual system configuration. It's currently deployed on **[Render](https://render.com)** using the free Docker web service tier.

---

## 📝 Notes & Limitations

- Maximum upload size: **16MB**
- OCR accuracy depends on image quality — clean, high-contrast screenshots work best
- Engagement analysis is intentionally **rule-based**, not ML-based — this keeps the app fast, dependency-light, and fully explainable (every suggestion maps to a transparent, inspectable rule rather than a black-box model)

---

## 👤 Author

**Rajesh Vinjam**

[![GitHub](https://img.shields.io/badge/GitHub-rajesh09999cloud-181717?style=flat-square&logo=github)](https://github.com/rajesh09999cloud?tab=repositories)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Rajesh%20Vinjam-0A66C2?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/rajesh-vinjam-5a2261320)

---

<div align="center">
<sub>Built as part of a technical assessment for a Software Engineer position.</sub>
</div>
