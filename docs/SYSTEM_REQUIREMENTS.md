# System Requirements

## Hardware Requirements

- Processor: Intel i3/i5 or higher
- RAM: Minimum 4GB, 8GB recommended
- Storage: 10GB free disk space
- Internet connection required

## Software Requirements

- Operating System: Windows, Linux, or macOS
- Python 3.10+
- Streamlit
- OpenAI Whisper
- Sentence-Transformers
- Librosa
- SoundFile
- Matplotlib
- ReportLab
- Torch
- NLTK
- Scikit-learn
- SQLite
- Git and GitHub
- Visual Studio Code or PyCharm

## Installation

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Additional Setup

- Install FFmpeg if Whisper transcription fails.
- Keep `uploads/` and `reports/` folders in the project root.
- Run the app from the project root so relative paths work correctly.

