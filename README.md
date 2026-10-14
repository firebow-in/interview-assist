# ⚜️ Luminal Insight | Interview Assist Dashboard

> A high-performance AI analytics platform for evaluating interview recordings with precision and visual clarity.

*by Tejas P*

---

## 🌟 Features

- **Luminal UI** — A professional dark-navy dashboard designed for depth and focus.
- **AI Composite Scoring** — A single "Match Score" (%) derived from weighted performance metrics.
- **Visual Analytics** — Matplotlib charts tuned for *Soft Skills* and *Technical* insight.
- **Precision ASR** — Transcription powered by OpenAI's Whisper model.
- **Feedback Intelligence** — Categorized Strengths (💠) and Areas for Improvement (⚠️) cards.
- **Universal Playability** — Automatic H.264/AAC re-encoding for seamless browser playback.

---

## 🎨 Design System

| Token | Value | Description |
|---|---|---|
| Primary Background | `#0b0d17` | Deep Space Navy |
| Accent Color | `#9d70ff` | Luminal Lavender |
| Typography | Sans-serif | Clean hierarchy for data readability |

---

## ▶️ Setup & Installation

### 1. Prerequisite: FFmpeg

Ensure **FFmpeg** is installed and added to your system `PATH`.

- **Windows**: [Download FFmpeg](https://ffmpeg.org/download.html)
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg`

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Launch

```bash
python app.py
```

---

## 📂 Project Structure

```
interview-assist/
├── app.py              # Main Gradio application entry point
├── requirements.txt    # Python dependencies
├── services/           # Core logic (ASR, Audio, Scoring)
├── utils/              # Support utilities (Text Cleaning)
├── data/
│   └── input/          # Staging area for uploaded media
└── docs/               # Project Design (PRD, Technical)
```

---

## 📌 Roadmap

- [ ] Radar charts for multi-dimensional profile comparison.
- [ ] LLM-based qualitative behavioral reasoning.
- [ ] History and multi-candidate comparison views.
- [ ] Exportable PDF Evaluation Reports.
