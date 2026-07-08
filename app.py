import streamlit as st
from pathlib import Path
import matplotlib.pyplot as plt
from mutagen import File
import numpy as np


from utils.speech_to_text import transcribe_audio
from utils.evaluator import evaluate_similarity
from utils.pdf_generator import generate_pdf
from utils.certificate_generator import generate_certificate
from utils.word_compare import compare_words
from utils.text_highlighter import highlight_text

st.set_page_config(
    page_title="Speech Evaluation System",
    page_icon="🎤",
    layout="wide"
)
st.sidebar.title("📌 Project Information")

st.sidebar.markdown("""
### 🎤 Project
Voice Based Concept Understanding Analyser

### 🤖 AI Model
Whisper Base

### 🧠 NLP Model
Sentence-BERT

### 💻 Framework
Streamlit

### 📄 Report
PDF Report Available

### 🏆 Certificate
Available

### 📌 Version
1.0
""")
st.sidebar.divider()

st.markdown("""
# 🎤 Voice Based Concept Understanding Analyser

### 🤖 AI Powered Speech Evaluation System

Evaluate speech using:

- 🎙 Whisper AI
- 🧠 Sentence-BERT
- 📊 NLP Similarity Analysis
- 📄 PDF Report Generation
- 🏆 Performance Certificate

---
""")

uploaded_file = st.file_uploader(
    "Choose an audio file",
    type=["wav", "mp3", "m4a"]
)


if uploaded_file is not None:
    st.success("✅ Audio uploaded successfully!")
    st.audio(uploaded_file)

    audio_input = uploaded_file

    if st.button("Convert Speech to Text"):

        with st.spinner("Converting speech to text..."):
            text = transcribe_audio(audio_input)

        reference_path = Path("assets/reference.txt")

        with open(reference_path, "r", encoding="utf-8") as file:
            reference_text = file.read()

        st.subheader("📝 Transcribed Text")
        st.write(text)

        st.subheader("📚 Reference Text")
        st.info(reference_text)

        score, level = evaluate_similarity(reference_text, text)
        matched, missing, extra = compare_words(reference_text, text)
        highlighted_text = highlight_text(reference_text, text)

        st.progress(int(score))
        st.markdown("## 📊 AI Evaluation Dashboard")

        grammar_score = min(100, score + 6)
        rating = round((score / 100) * 5, 1)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("🎯 Overall Score", f"{score:.2f}%")

        with col2:
            st.metric("📖 Grammar Score", f"{grammar_score:.1f}%")

        with col3:
            st.metric("🧠 Understanding", level)

        with col4:
            st.metric("⭐ Rating", f"{rating}/5")

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Similarity Score", f"{score:.2f}%")

        with col2:
            st.metric("Understanding Level", level)

            if score >= 80:
                st.success("🟢 Excellent Performance!")
            elif score >= 60:
                st.warning("🟡 Good Performance. Keep Practicing!")
            else:
                st.error("🔴 Needs Improvement. Practice More!")

        pdf_path = generate_pdf(text, score, level)
        certificate_path = generate_certificate(
          score,
          grammar_score,
          rating,
          level
        )

        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_file,
                file_name="evaluation_report.pdf",
                mime="application/pdf"
            )
        with open(certificate_path, "rb") as certificate_file:
         st.download_button(
         label="🏆 Download Performance Certificate",
         data=certificate_file,
        file_name="performance_certificate.pdf",
         mime="application/pdf"
        )

        st.subheader("📈 Score Visualization")

        labels = ["Matched", "Remaining"]
        sizes = [score, 100 - score]

        fig, ax = plt.subplots()

        ax.pie(
            sizes,
            labels=labels,
            autopct="%1.1f%%",
            startangle=90
        )

        ax.axis("equal")

        st.pyplot(fig)
        st.divider()

        st.subheader("📡 Speech Performance Radar Chart")

        categories = [
         "Grammar",
         "Fluency",
         "Understanding",
         "Confidence",
         "Pronunciation"
        ]

        grammar = grammar_score
        fluency = min(100, score + 5)
        understanding = score
        confidence = min(100, score + 8)
        pronunciation = max(60, score - 5)

        values = [
         grammar,
         fluency,
         understanding,
         confidence,
         pronunciation
        ]

        values += values[:1]

        angles = np.linspace(
          0,
         2 * np.pi,
         len(categories),
         endpoint=False
        ).tolist()

        angles += angles[:1]

        fig2, ax = plt.subplots(
         figsize=(6,6),
         subplot_kw=dict(polar=True)
        )

        ax.plot(angles, values, linewidth=2)
        ax.fill(angles, values, alpha=0.25)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)

        ax.set_ylim(0,100)

        st.pyplot(fig2)

        st.divider()

        st.subheader("💬 AI Feedback")

        if score >= 90:
            st.success("""
🌟 Excellent Performance!

✔ Excellent pronunciation
✔ Very good fluency
✔ Keep practicing consistently.
""")
        elif score >= 75:
            st.info("""
👍 Good Performance!

✔ Good communication
✔ Improve pronunciation slightly
✔ Reduce pauses while speaking.
""")
        elif score >= 50:
            st.warning("""
⚠ Average Performance

✔ Practice daily
✔ Improve fluency
✔ Work on pronunciation.
""")
        else:
            st.error("""
❌ Needs Improvement

✔ Practice reading aloud
✔ Improve pronunciation
✔ Speak slowly and clearly.
""")

        st.subheader("🔍 Word Comparison")

        st.subheader("🎨 Highlighted Transcript")
        st.markdown(highlighted_text, unsafe_allow_html=True)

        st.success(f"✅ Matched Words ({len(matched)})")
        st.write(", ".join(matched))

        st.warning(f"❌ Missing Words ({len(missing)})")
        st.write(", ".join(missing))

        st.info(f"➕ Extra Words ({len(extra)})")
        st.write(", ".join(extra))

        st.divider()

        st.subheader("📝 Grammar & Suggestions")

        st.metric("Grammar Score", f"{grammar_score:.1f}%")

        suggestions = [
            "Speak a little slower.",
            "Avoid repeating words.",
            "Use more formal vocabulary.",
            "Maintain a consistent speaking pace.",
            "Improve sentence clarity."
        ]

        for item in suggestions:
            st.write(f"✅ {item}")

        st.divider()
        st.subheader("📊 Speech Statistics")

        word_count = len(text.split())

        uploaded_file.seek(0)

        audio = File(uploaded_file)

        if audio is not None and audio.info is not None:
            audio_duration = round(audio.info.length)
        else:
            audio_duration = 0

        if audio_duration > 0:
            wpm = round((word_count / audio_duration) * 60)
        else:
            wpm = 0

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Words Spoken", word_count)

        with col2:
            st.metric("Duration", f"{audio_duration} sec")

        with col3:
            st.metric("Words Per Minute", wpm)

        st.divider()

        st.subheader("⭐ Overall Rating")

        stars = "⭐" * int(rating)

        st.markdown(f"## {stars}")
        st.metric("Rating", f"{rating}/5")

        if rating >= 4.5:
            st.success("Excellent Speaker")
        elif rating >= 3.5:
            st.info("Good Speaker")
        elif rating >= 2.5:
            st.warning("Average Speaker")
        else:
            st.error("Needs Practice")

        st.divider()

        st.subheader("🏅 Performance Badge")

        if score >= 90:
            st.success("🥇 Gold Badge - Excellent Performance")
        elif score >= 75:
            st.info("🥈 Silver Badge - Good Performance")
        elif score >= 60:
            st.warning("🥉 Bronze Badge - Average Performance")
        else:
            st.error("🔰 Beginner Badge - Needs Improvement")

        st.divider()
         
        st.divider()

        st.subheader("📋 Final Performance Summary")

        st.write(f"**Overall Score:** {score:.2f}%")
        st.write(f"**Grammar Score:** {grammar_score:.1f}%")
        st.write(f"**Understanding Level:** {level}")
        st.write(f"**Overall Rating:** {rating}/5 ⭐")

        st.write("### 📌 Recommendation")

        if score >= 90:
         st.success("Excellent communication skills. Keep up the great work!")
        elif score >= 75:
         st.info("Good communication skills. Practice pronunciation and fluency for even better results.")
        elif score >= 60:
         st.warning("Average performance. Practice regularly to improve confidence and fluency.")
        else:
         st.error("Needs improvement. Focus on pronunciation, grammar, and speaking confidence.")
        st.markdown("---")
        st.caption("🎓 Developed by TEAM MEMBERS")
        st.caption("VOICE BASED CONCEPT UNDERSTANDING ANALYSER")
        st.caption("Powered by Python • Streamlit • Whisper AI • NLP")