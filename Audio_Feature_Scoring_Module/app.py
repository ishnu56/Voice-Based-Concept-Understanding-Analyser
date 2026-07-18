import json
import os
from pathlib import Path
import time
import uuid
import streamlit as st
import pandas as pd

from modules.speech_to_text import transcribe_audio
from modules.semantic_analysis import semantic_similarity
from modules.filler_detector import detect_filler_words
from modules.audio_features import extract_audio_features, save_waveform
from modules.scoring import evaluate_understanding
from modules.ai_feedback import generate_feedback
from modules.pdf_generator import generate_pdf_report
from database.database import save_result, get_recent_results, init_db

BASE = Path(__file__).resolve().parent
UPLOAD_DIR = BASE / "uploads"
REPORT_DIR = BASE / "reports"
ASSET_DIR = BASE / "assets"
for p in [UPLOAD_DIR, REPORT_DIR, ASSET_DIR]:
    p.mkdir(exist_ok=True)

st.set_page_config(page_title="VBCUA", page_icon="V", layout="wide")
css = ASSET_DIR / "style.css"
if css.exists():
    st.markdown(f"<style>{css.read_text()}</style>", unsafe_allow_html=True)

@st.cache_data
def load_concepts():
    with open(BASE / "concepts.json", "r", encoding="utf-8") as f:
        return json.load(f)

concepts = load_concepts()
init_db()
if "analysis" not in st.session_state:
    st.session_state["analysis"] = None
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())

st.markdown(
    """
    <div class="hero-card">
        <div class="eyebrow">AI Educational Assessment Dashboard</div>
        <div class="main-title">Voice-Based Concept Understanding Analyser</div>
        <div class="subtitle">Evaluates conceptual understanding from spoken explanations using AI-powered transcription, semantic analysis, audio features, scoring, and reporting.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns([1.4, 1])
with left:
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    user_name = st.text_input("User / Student Name", value="Student")
    topic = st.selectbox("Select Reference Concept", list(concepts.keys()))
    uploaded = st.file_uploader("Upload Student Audio (WAV/MP3)", type=["wav", "mp3", "m4a"])
    if uploaded:
        suffix = Path(uploaded.name).suffix.lower()
        if suffix not in {".wav", ".mp3", ".m4a"}:
            st.error("Invalid audio format. Please upload WAV, MP3, or M4A.")
            audio_path = None
        else:
            safe_name = f"{int(time.time())}_{uploaded.name}"
            audio_path = UPLOAD_DIR / safe_name
            audio_path.write_bytes(uploaded.getbuffer())
            st.audio(str(audio_path))
    else:
        audio_path = None
        st.info("Upload an audio file to begin analysis.")
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.subheader("Concept Reference")
    st.write(concepts[topic])
    st.caption("Reference concept repository is loaded from concepts.json")
    st.markdown('</div>', unsafe_allow_html=True)

if uploaded and st.button("Analyze Concept Understanding", type="primary"):
    with st.spinner("Processing and evaluating..."):
        if audio_path is None:
            st.error("Please upload a valid audio file.")
            st.stop()

        started = time.perf_counter()
        transcript_result = transcribe_audio(str(audio_path))
        transcription_runtime = round(time.perf_counter() - started, 3)
        transcript = transcript_result["text"]

        if not transcript_result["success"]:
            st.warning(transcript_result["error"])
            st.info("Automatic transcription failed, so scoring is paused until valid transcription is available.")
            st.session_state["analysis"] = None
            st.stop()

        reference = concepts[topic]
        started = time.perf_counter()
        similarity = semantic_similarity(transcript, reference)
        embedding_runtime = round(time.perf_counter() - started, 3)
        filler = detect_filler_words(transcript)
        started = time.perf_counter()
        audio = extract_audio_features(str(audio_path))
        audio_feature_runtime = round(time.perf_counter() - started, 3)
        if audio.get("error"):
            st.error(f"Could not extract audio features: {audio['error']}")
            st.stop()

        waveform_path = REPORT_DIR / f"waveform_{audio_path.stem}.png"
        save_waveform(str(audio_path), str(waveform_path))
        result = evaluate_understanding(similarity, filler["filler_ratio"], audio)
        feedback = generate_feedback(similarity, filler, audio, result)

        pdf_path = REPORT_DIR / f"VBCUA_Report_{audio_path.stem}.pdf"
        metrics = {
            "Semantic Similarity": similarity,
            "Filler Word Ratio": filler["filler_ratio"],
            "Total Filler Words": filler["total_fillers"],
            "Pause Ratio": audio.get("pause_ratio"),
            "RMS Energy": audio.get("rms_energy"),
            "Zero Crossing Rate": audio.get("zero_crossing_rate"),
            "Duration": audio.get("duration"),
            "Transcription Runtime": f"{transcription_runtime}s",
            "Embedding Runtime": f"{embedding_runtime}s",
            "Audio Feature Runtime": f"{audio_feature_runtime}s",
            "Final Score": f"{result['score']}/100",
            "Understanding Level": result["level"],
        }
        generate_pdf_report(str(pdf_path), {
            "reference": reference,
            "transcript": transcript,
            "waveform_path": str(waveform_path),
            "metrics": metrics,
            "feedback": feedback,
        })
        save_result(
            topic,
            transcript,
            similarity,
            filler["filler_ratio"],
            audio.get("pause_ratio"),
            audio.get("rms_energy"),
            result["score"],
            result["level"],
            user_name=user_name,
            audio_file=audio_path.name,
            filler_count=filler["total_fillers"],
            zero_crossing_rate=audio.get("zero_crossing_rate"),
            duration=audio.get("duration"),
            transcription_runtime=transcription_runtime,
            embedding_runtime=embedding_runtime,
            audio_feature_runtime=audio_feature_runtime,
            report_path=str(pdf_path),
            session_id=st.session_state["session_id"],
        )
        st.session_state["analysis"] = dict(
            user_name=user_name,
            audio_file=audio_path.name,
            transcript=transcript,
            reference=reference,
            similarity=similarity,
            filler=filler,
            audio=audio,
            waveform_path=str(waveform_path),
            result=result,
            feedback=feedback,
            pdf_path=str(pdf_path),
            metrics=metrics,
            runtimes={
                "Transcription": transcription_runtime,
                "Embedding": embedding_runtime,
                "Audio Features": audio_feature_runtime,
            },
        )

analysis = st.session_state.get("analysis")
if analysis:
    st.markdown(f'<div class="{analysis["result"]["css_class"]}">Analysis Completed</div>', unsafe_allow_html=True)
    c1, c2 = st.columns([1.2, 1])
    with c1:
        st.subheader("Transcribed Explanation")
        st.write(analysis["transcript"])
        st.image(analysis["waveform_path"], caption="Audio Waveform")
    with c2:
        st.subheader("Final Evaluation")
        st.metric("Understanding Score", f"{analysis['result']['score']}/100")
        st.progress(min(100, int(analysis["result"]["score"])) / 100)
        st.markdown(f"### {analysis['result']['level']}")
        st.subheader("AI Feedback")
        st.markdown(f'<div class="feedback-box">{analysis["feedback"]}</div>', unsafe_allow_html=True)
    st.subheader("Evaluation Metrics")
    st.dataframe(pd.DataFrame(list(analysis["metrics"].items()), columns=["Metric", "Value"]), use_container_width=True)
    with open(analysis["pdf_path"], "rb") as f:
        st.download_button("Download PDF Report", f, file_name=os.path.basename(analysis["pdf_path"]), mime="application/pdf")

st.divider()
st.subheader("Recent Evaluation History")
rows = get_recent_results()
if rows:
    st.table(pd.DataFrame(rows, columns=["Date", "Concept", "Score", "Understanding Level"]))
else:
    st.caption("No evaluations saved yet.")
