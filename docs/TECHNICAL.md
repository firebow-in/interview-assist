# Technical Design — Luminal Insight Dashboard

## 🏗️ UI Architecture

The "Luminal Insight" dashboard is built using **Gradio Blocks**, a lightweight and responsive UI framework that enables complex, low-latency data visualization.

### Data Visualization Logic
- **Matplotlib Integration**: A custom bar chart renderer is implemented to visualize four core performance metrics:
    - **Task Completion**
    - **Communication**
    - **Output Quality**
    - **Judgement**
- **Match Score Calculation**: A composite scoring algorithm that averages all four metrics into a single percentage, providing a high-level "AI-driven Match Score."

---

## 🧰 Tech Stack

*   **Python 3.10+**: Runtime logic.
*   **Gradio (UI Framework)**: Custom CSS-injected theme for the dark navy dashboard.
*   **Whisper (ASR)**: Speech-to-text processing for high-fidelity transcripts.
*   **Matplotlib & Numpy**: Dynamic charting and metric normalization.
*   **MoviePy (FFmpeg)**: Audio extraction and browser-safe re-encoding (libx264/aac).

---

## 📁 Updated Project Structure

```bash
interview-assist/
├── app.py             # Dashboard UI (Luminal Insight Theme)
├── requirements.txt   # Dependencies (inc. matplotlib, numpy)
├── services/          # Business Logic
│   ├── audio.py       # Extraction & Playability Encoding
│   ├── asr.py         # Transcription interface
│   └── scoring.py     # Rule-based analytics engine
├── utils/             # Support
│   └── text_cleaner.py # Transcript normalization
└── data/ input/       # Media staging area
```

---

## 🔄 Core Processing Modules

### `audio.py` — Multi-Phase Extraction
1. **Local Staging**: Copies the uploaded file to `data/input` to prevent OS-level access conflicts.
2. **Audio Extraction**: Extracts a high-quality MP3 for Whisper processing.
3. **Playability Check**: Re-encodes using Libx264/AAC if needed for browser-safe video playback.

### `asr.py` — Intelligence Layer
- **Whisper Base**: Optimized for high speed and accuracy on CPU environments.

### `scoring.py` — Analytics Engine
- **Pattern Matching**: Detects filler words and relevant keywords.
- **Scoring Logic**: Translates text properties into normalized integer ratings (1-10).

---

## ⚙️ Dependencies

*   `gradio`: Premium UI Shell
*   `openai-whisper`: ASR Intelligence
*   `moviepy`: Media Processing
*   `matplotlib` & `numpy`: Visual Analytics
*   `ffmpeg-python`: FFmpeg Interface

---

## 🔐 Performance Strategy

- **Onside Staging**: Files are processed locally within the working directory to ensure data persistency during analysis.
- **Lazy Loading**: Visual assets (charts) are generated only upon analysis completion to reduce overhead.
