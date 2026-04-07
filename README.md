# Interview Questions Generator 📋

An AI-powered Streamlit application that generates professional interview questions and answers using Google's Gemini API, enriched with real-time web data via the FireCrawl API. Outputs can be exported as formatted PDF or Word documents with partner institute branding.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Usage Guide](#usage-guide)
- [API Keys](#api-keys)
- [Deployment on Streamlit Cloud](#deployment-on-streamlit-cloud)
- [Module Reference](#module-reference)
- [Known Limitations](#known-limitations)
- [Troubleshooting](#troubleshooting)

---

## Overview

The Interview Questions Generator is a web-based tool designed for educators and training professionals. Given a topic, a difficulty level, and curriculum content, it uses the Gemini LLM to generate a set of interview Q&A pairs split between conceptual ("generic") and hands-on ("practical") questions. It optionally fetches up-to-date context from the web via FireCrawl before generation. The finished question set can be reviewed and edited in the browser, then exported as a branded PDF or Word document.

---

## Features

- **AI-Powered Generation** — Uses Google Gemini 1.5 Flash for fast, high-quality Q&A generation.
- **Web-Enriched Context** — Optionally scrapes current articles via FireCrawl to keep questions up to date.
- **Configurable Parameters** — Topic, difficulty (Beginner / Intermediate / Advanced), question count (1–15), and practical/generic split.
- **In-Browser Review & Edit** — Edit any question or answer before exporting.
- **PDF Export** — Branded cover page + content pages via WeasyPrint.
- **Word Document Export** — Fully formatted `.docx` with blue cover page and partner logo via python-docx.
- **Partner Institute Branding** — Supports IIT Kanpur and IIT Guwahati logos out of the box.
- **Retry Logic** — Automatic retries with exponential backoff on Gemini rate limits.

---

## Project Structure

```
Interview_Questions_Generator/
│
├── app.py                        # Main Streamlit application
├── config.py                     # App-wide constants and settings
├── requirements.txt              # Python dependencies
├── packages.txt                  # System-level apt packages (for Streamlit Cloud)
├── .gitignore
│
├── assets/
│   └── logos/
│       ├── iitk-accredian-banner.png
│       └── iitg-accredian-banner.png
│
├── utils/
│   ├── __init__.py               # Makes utils a proper Python package
│   ├── gemini_service.py         # Gemini API wrapper + Q&A parser
│   ├── firecrawl_service.py      # FireCrawl web scraping wrapper
│   ├── prompt_templates.py       # Prompt construction for Gemini
│   ├── document_generator.py     # PDF (WeasyPrint) + Word (python-docx) generators
│   ├── company_template.py       # Logo URL/path mappings per partner institute
│   └── important_words_detector.py  # Keyword extractor (utility, not used in main flow)
│
└── .devcontainer/
    └── devcontainer.json         # GitHub Codespaces configuration
```

---

## Prerequisites

- Python 3.9 or higher
- A [Google Gemini API key](https://aistudio.google.com/app/apikey) (free tier available)
- A [FireCrawl API key](https://www.firecrawl.dev/) (free tier available)
- On Linux/macOS, the WeasyPrint system packages listed in `packages.txt` must be installed

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/Interview_Questions_Generator.git
cd Interview_Questions_Generator
```

### 2. Create and activate a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 3. Install system packages (Linux only — required for WeasyPrint PDF export)

```bash
sudo apt update
sudo xargs -a packages.txt apt install -y
```

### 4. Install Python dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration

All tunable constants live in `config.py`:

| Constant | Default | Description |
|---|---|---|
| `GEMINI_MODEL` | `gemini-1.5-flash` | Gemini model used for generation |
| `GEMINI_MAX_TOKENS` | `4000` | Max output tokens per request |
| `GEMINI_TEMPERATURE` | `0.4` | Sampling temperature (lower = more deterministic) |
| `MIN_QUESTIONS` | `1` | Minimum questions per generation |
| `MAX_QUESTIONS` | `15` | Maximum questions per generation |
| `MIN_ANSWER_WORDS` | `80` | Minimum words per answer |
| `MAX_ANSWER_WORDS` | `150` | Maximum words per answer |
| `FIRECRAWL_TIMEOUT` | `60` | Seconds before FireCrawl scrape times out |

---

## Running the Application

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## Usage Guide

### Tab 1 — Generate

1. Enter your **Gemini** and **FireCrawl API keys** in the sidebar.
2. Fill in:
   - **Topic Name** — e.g., *Machine Learning Algorithms*
   - **Number of Questions** — slider from 1 to 15
   - **Difficulty Level** — Beginner / Intermediate / Advanced
   - **Practical Questions %** — percentage of questions that should be scenario/application-based
   - **Partner Institute** — branding for the exported document
   - **Curriculum Content** — paste relevant syllabus or course material
3. Click **🚀 Generate**.

The app will:
- Optionally fetch two recent web articles related to the topic via FireCrawl.
- Build a structured prompt and call the Gemini API.
- Retry up to 3 times if the exact question count is not returned.
- Display success/failure and the generic vs. practical split.

### Tab 2 — Review & Edit

- Expand any question card to edit the question or answer text.
- Changes are saved to session state and reflected in the exported document.

### Tab 3 — Export

1. Choose **PDF** or **Word Document**.
2. Click **Generate** to render the document.
3. Click **Download** to save the file locally.

Document naming format: `Interview_Questions_<Topic>_<YYYYMMDD_HHMMSS>.(pdf|docx)`

---

## API Keys

Both API keys are entered at runtime through the sidebar and are never stored or logged.

| Key | Where to get it | Free tier |
|---|---|---|
| Gemini API Key | [Google AI Studio](https://aistudio.google.com/app/apikey) | Yes |
| FireCrawl API Key | [firecrawl.dev](https://www.firecrawl.dev/) | Yes (500 credits/month) |

> **Note:** FireCrawl is used only for web context enrichment. If the scrape fails, the app falls back gracefully to generating questions from the curriculum content alone.

---

## Deployment on Streamlit Cloud

1. Push this repository to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and create a new app pointing to `app.py`.
3. Streamlit Cloud will automatically install system packages from `packages.txt` and Python packages from `requirements.txt`.
4. No secrets need to be pre-configured — users enter their API keys at runtime.

---

## Module Reference

### `app.py`
Main Streamlit application. Manages session state, UI layout (three tabs), and orchestrates calls to `GeminiService`, `FireCrawlService`, `PDFGenerator`, and `WordDocumentGenerator`.

### `config.py`
Central store for all constants. Modify this file to change model settings, token limits, question count bounds, or answer length targets without touching business logic.

### `utils/gemini_service.py`
- `GeminiService(api_key)` — configures the `google-generativeai` client.
- `generate_questions(prompt)` — sends the prompt to Gemini with retry/backoff for 429 (rate limit) and 503 (overloaded) responses. Falls back from `gemini-1.5-flash` to `gemini-pro` on 404.
- `parse_qa_pairs(response_text, expected_count)` — parses the `QUESTION N / ANSWER N` format returned by Gemini into a list of dicts with keys `id`, `question`, `answer`, `type`.

### `utils/firecrawl_service.py`
- `FireCrawlService(api_key)` — wraps the `FirecrawlApp` SDK client.
- `scrape_url(url)` — scrapes a single URL and returns markdown text.
- `search_and_scrape(query, max_results)` — runs a web search and scrapes the top results.

### `utils/prompt_templates.py`
- `get_question_generation_prompt(...)` — builds the structured Gemini prompt that enforces the exact question count, type labels `(GENERIC)` / `(PRACTICAL)`, and answer word-count targets.

### `utils/document_generator.py`
- `PDFGenerator(title, topic, partner_institute)` — generates a PDF using WeasyPrint with a branded cover page and Q&A content pages.
- `WordDocumentGenerator()` — generates a `.docx` file with a blue cover page and institute logo using python-docx.

### `utils/company_template.py`
Maps partner institute names to:
- `PARTNER_LOGO_URLS` — remote URLs used by WeasyPrint for the PDF cover.
- `PARTNER_LOGOS` — local file paths (relative to project root) used by python-docx for the Word cover.

### `utils/important_words_detector.py`
- `ImportantWordsDetector` — keyword detector that scans answer text for a predefined list of technical terms. Not used in the main generation flow; available for extension.

---

## Known Limitations

- **Question count accuracy** — Gemini may occasionally generate fewer questions than requested despite retries. The app reports the actual count and flags the mismatch.
- **WeasyPrint on Windows** — WeasyPrint has complex native dependencies on Windows. PDF export is most reliable on Linux (including Streamlit Cloud and Codespaces). Use Word export on Windows.
- **FireCrawl quota** — The free FireCrawl tier allows 500 credits/month. Web enrichment is best-effort; the app will still generate questions without it.
- **Gemini rate limits** — Free-tier Gemini API keys are subject to per-minute rate limits. The app uses exponential backoff (10 s, 20 s, 40 s) but very rapid successive generations may still hit quota errors.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `ImportError: cannot import name 'FirecrawlApp'` | Outdated `firecrawl-py` | `pip install --upgrade firecrawl-py` |
| `ModuleNotFoundError: No module named 'utils'` | `utils/__init__.py` missing | Ensure `utils/__init__.py` exists in the repo |
| PDF export fails silently | WeasyPrint system deps missing | Run `sudo xargs -a packages.txt apt install -y` |
| Word logo is missing | Logo file not found | Confirm `assets/logos/` contains the `.png` files |
| `❌ Generated N but requested M` | Gemini truncated output | Reduce question count or try again |
| `⚠️ API Busy: Rate limit reached` | Gemini 429 quota | Wait 1–2 minutes and try again |
