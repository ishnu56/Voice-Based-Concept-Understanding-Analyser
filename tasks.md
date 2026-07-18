# VBCUA Assigned Task - Epics and Stories

## Epic 1: Environment Setup and Configuration

### Story 1: Python Environment and Dependency Installation

- Configure Python 3.10+ environment.
- Install required dependencies listed in `requirements.txt`.
- Include Streamlit, OpenAI Whisper, Sentence-Transformers, Librosa, SoundFile, NumPy, Matplotlib, ReportLab, Torch, NLTK, Pytest, and Scikit-learn.
- Verify successful installation and compatibility of all modules.

### Story 2: Project Structure Initialization

- Organize the project into a clean modular structure.
- Maintain clear separation between UI, audio processing, semantic analysis, scoring, reporting, and documentation.

Main files:

- `app.py` - Streamlit front-end and main application logic
- `modules/audio_features.py` - Audio loading, waveform generation, and feature extraction
- `modules/speech_to_text.py` - Whisper-based transcription logic
- `modules/semantic_analysis.py` - Semantic similarity computation using Sentence-BERT
- `modules/filler_detector.py` - Filler word detection and filler ratio calculation
- `modules/scoring.py` - Understanding score calculation and classification
- `modules/pdf_generator.py` - PDF report generation using ReportLab

### Story 3: Streamlit Application Initialization

- Launch the application using `streamlit run app.py`.
- Validate interaction between Streamlit UI and backend modules.
- Ensure uploaded audio triggers transcription, analysis, visualization, scoring, and report generation.

## Epic 2: Core Logic Development - Understanding and Evaluation Engine

### Story 1: Speech-to-Text Module Development

- Integrate OpenAI Whisper to convert uploaded audio files into text.
- Support common audio formats such as WAV, MP3, and M4A.
- Handle missing FFmpeg, invalid audio, and transcription errors gracefully.

### Story 2: Semantic Understanding and Similarity Engine

- Generate Sentence-BERT embeddings for student explanations and reference concepts.
- Compute cosine similarity scores to quantify conceptual alignment.
- Normalize similarity values for consistent interpretation.

### Story 3: Audio Feature Extraction and Scoring Engine Development

- Extract audio-level features such as duration, RMS energy, pause ratio, and zero crossing rate using Librosa and SoundFile.
- Implement filler word detection to compute filler word ratio from transcribed text.
- Combine semantic similarity, filler usage, and audio confidence metrics into a final understanding score.
- Classify results as Strong Understanding, Moderate Understanding, or Poor Understanding.

## Epic 3: Streamlit UI Implementation and Interaction

### Story 1: User Interface Design and Visualization

- Design a structured Streamlit dashboard for reference concepts, audio upload, waveform visualization, metrics, and final results.
- Apply white and dark-blue professional styling suitable for an AI educational assessment dashboard.

### Story 2: Input Handling and Session State Management

- Implement audio upload controls, action buttons, and dynamic result rendering.
- Use Streamlit session state to persist transcript, audio features, score, evaluation result, and report path.
- Validate unsupported or corrupted audio files gracefully.

### Story 3: Output Rendering and Report Generation

- Display transcribed explanation, semantic similarity score, filler word ratio, audio metrics, and final understanding score.
- Render waveform visualization for transparency in audio analysis.
- Generate downloadable PDF reports containing reference concept, transcript, waveform image, evaluation metrics, and qualitative feedback.

## Epic 4: Testing, Optimization, and Deployment

### Story 1: Functional Testing and Validation

- Test audio upload, waveform rendering, action buttons, metrics display, and report download.
- Validate transcription, semantic similarity scoring, filler detection, and evaluation consistency.

### Story 2: Performance Testing and Optimization

- Measure runtime performance for transcription, embedding computation, and audio feature extraction.
- Optimize model loading using Streamlit caching.
- Ensure stability for repeated evaluations and longer audio inputs.

### Story 3: Deployment Preparation and Final Review

- Prepare the application for local deployment or Streamlit Cloud deployment.
- Conduct final end-to-end testing from audio input to PDF output.
- Verify error handling and safe fallback mechanisms before release.

## Outcome

By completing this assigned module, the project demonstrates:

- AI-based spoken concept assessment
- Whisper transcription integration
- Sentence-BERT semantic similarity analysis
- Fluency evaluation using audio features and filler word detection
- Automated scoring and feedback generation
- Downloadable PDF reporting
- A responsive Streamlit interface for final-year engineering project demonstration

