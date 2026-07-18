# Project Template Checklist

## Project

**Voice-Based Concept Understanding Analyser (VBCUA)**

## Interface Requirements

- Title: Voice-Based Concept Understanding Analyser
- Subtitle explaining AI-based conceptual understanding evaluation
- Clean white and dark-blue professional dashboard theme
- Dropdown for reference concepts
- Student audio upload
- Built-in audio player
- Analyze Concept Understanding button
- Processing spinner
- Audio waveform graph
- Student transcript display
- Semantic similarity score
- Audio feature metrics
- Colored progress bar for overall score
- Understanding level: Strong, Moderate, Poor
- AI-generated feedback box
- Download PDF report button

## Audio Features

- Duration
- RMS Energy
- Pause Ratio
- Zero Crossing Rate

## Database And History

SQLite database stores evaluation records and supports:

- User
- Audio File
- Transcript
- Reference Concept
- Semantic Similarity
- Audio Feature
- Evaluation Result
- Report
- Session
- Filler Word Statistics

Recent Evaluation History displays:

- Date
- Concept
- Score
- Understanding Level

## Engineering Requirements

- Audio format validation
- Graceful handling of invalid or corrupted audio
- Streamlit session state
- Streamlit caching for model loading
- Runtime measurement for transcription, embedding, and audio feature extraction
- Repeated evaluations
- Automatic creation of `uploads/` and `reports/`
- Automatic waveform image generation
- Downloadable PDF report generation

## Technology Stack

- Python
- Streamlit
- OpenAI Whisper
- Sentence Transformers
- Librosa
- Scikit-learn
- SQLite
- Matplotlib
- ReportLab
