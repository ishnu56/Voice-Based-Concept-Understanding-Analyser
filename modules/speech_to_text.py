import os
import streamlit as st


@st.cache_resource(show_spinner=False)
def load_whisper_model(model_name: str = "base"):
    import whisper

    return whisper.load_model(model_name)


def transcribe_audio(audio_path: str, model_name: str = "base") -> dict:
    """Transcribe audio using OpenAI Whisper.

    A safe fallback message is returned if Whisper or ffmpeg is unavailable, so the
    rest of the application can still be demonstrated during review.
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    try:
        model = load_whisper_model(model_name)
        result = model.transcribe(audio_path)
        return {
            "text": result.get("text", "").strip(),
            "success": True,
            "error": "",
        }
    except Exception as exc:
        return {
            "text": "",
            "success": False,
            "error": (
                "Transcription could not be generated automatically. "
                "Please ensure openai-whisper and ffmpeg are installed correctly. "
                f"Technical detail: {exc}"
            ),
        }
