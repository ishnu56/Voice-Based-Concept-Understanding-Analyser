# VBCUA - Assigned Task Module

## Voice-Based Concept Understanding Analyser

This repository contains the assigned task implementation for the **Voice-Based Concept Understanding Analyser (VBCUA)** project.

## Assigned To

**Pathan Sadiya**

## Assigned Module

**Audio Feature Analysis, Input Handling, Scoring Integration, and Performance Optimization**

## Module Description

This module handles the audio-processing and evaluation workflow of VBCUA. It accepts student speech audio, validates the file, generates waveform visualization, extracts audio features, detects filler words, calculates semantic similarity, generates a final understanding score, and creates a downloadable PDF evaluation report.

## Features Implemented

- Student audio upload
- Audio format validation
- Built-in audio player
- Audio waveform generation
- Speech transcription using OpenAI Whisper
- Semantic similarity using Sentence-BERT
- Filler word detection
- Audio feature extraction:
  - Duration
  - RMS Energy
  - Pause Ratio
  - Zero Crossing Rate
- Final understanding score
- Understanding level classification:
  - Strong Understanding
  - Moderate Understanding
  - Poor Understanding
- AI-generated feedback
- PDF report generation
- Runtime measurement for:
  - Transcription
  - Embedding computation
  - Audio feature extraction
- Streamlit session state support
- Cached model loading
- Repeated evaluation support

## Technology Stack

- Python
- Streamlit
- OpenAI Whisper
- Sentence Transformers
- Librosa
- Scikit-learn
- Matplotlib
- ReportLab

## Project Structure

```text
VBCUA_Pathan_Sadiya_Assigned_Task/
├── app.py
├── concepts.json
├── requirements.txt
├── tasks.md
├── modules/
│   ├── audio_features.py
│   ├── filler_detector.py
│   ├── scoring.py
│   ├── semantic_analysis.py
│   ├── speech_to_text.py
│   ├── ai_feedback.py
│   └── pdf_generator.py
├── database/
│   └── database.py
├── assets/
│   └── style.css
├── uploads/
│   └── README.md
├── reports/
│   └── README.md
└── docs/
    ├── PROJECT_TEMPLATE_CHECKLIST.md
    ├── SYSTEM_REQUIREMENTS.md
    ├── CONCLUSION.md
    └── VBCUA_Pathan_Sadiya_Project_Documentation.docx
```

## How To Run

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL shown in the terminal:

```text
http://localhost:8501
```

## Template Documentation

The `docs/` folder contains the assigned-task project documentation prepared according to the provided project template format.

The `tasks.md` file maps the assigned work to the required epics and stories:

- Environment Setup and Configuration
- Core Logic Development
- Streamlit UI Implementation
- Testing, Optimization, and Deployment

## Note

Install FFmpeg if Whisper transcription does not work. The app includes fallback handling for missing model dependencies and invalid audio files.
