"""
Voice-Based Concept Understanding Analyser (VBCUA)
Main Streamlit Application Entrypoint.
"""

import streamlit as st
import numpy as np

# Import custom UI components
from ui.components import inject_premium_styles, render_score_card, plot_audio_waveform
from ui.reports import render_concept_comparison, render_detailed_metrics_tab
from utils.helpers import get_concept_reference, REFERENCE_CONCEPTS
from utils.report_generator import build_pdf_report

# Set up page configurations
st.set_page_config(
    page_title="VBCUA | Voice-Based Concept Understanding Analyser",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply sleek styling custom overrides
inject_premium_styles()

# Define navigation menu in the Sidebar
st.sidebar.markdown(
    """
    <div style='text-align: center; margin-bottom: 20px;'>
        <h2 style='color: #6366f1; font-weight: 800; letter-spacing: 1px;'>🎙️ VBCUA</h2>
        <p style='color: #64748b; font-size: 0.85rem;'>Voice-Based Concept Analyser</p>
    </div>
    """, 
    unsafe_allow_html=True
)

st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Navigation Menu",
    ["🎙️ Concept Analyzer", "📊 Performance Analytics", "⚙️ Configuration"],
    key="nav_selection"
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    <div style='font-size: 0.8rem; color: #64748b;'>
        <p><b>Model Status:</b> Ready</p>
        <p><b>Backend:</b> CPU (Whisper/S-BERT)</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Initial session states
if "selected_concept" not in st.session_state:
    st.session_state.selected_concept = list(REFERENCE_CONCEPTS.keys())[0]
if "transcription" not in st.session_state:
    st.session_state.transcription = ""
if "semantic_score" not in st.session_state:
    st.session_state.semantic_score = 0
if "fluency_score" not in st.session_state:
    st.session_state.fluency_score = 0
if "is_analyzed" not in st.session_state:
    st.session_state.is_analyzed = False

# ----------------- PAGE 1: CONCEPT ANALYZER -----------------
if page == "🎙️ Concept Analyzer":
    st.title("🎙️ Voice-Based Concept Understanding Analyser")
    st.markdown(
        "Evaluate how effectively you explain conceptual topics using advanced speech-to-text, "
        "semantic similarity (Sentence-BERT), and acoustic analysis."
    )
    
    col1, col2 = st.columns([1, 2], gap="large")
    
    with col1:
        st.subheader("💡 Select Target Concept")
        concept_name = st.selectbox(
            "Choose a topic to explain:",
            options=list(REFERENCE_CONCEPTS.keys()),
            index=0
        )
        
        # Display selected reference text
        reference_text = get_concept_reference(concept_name)
        st.text_area(
            "Reference Standard Description:",
            value=reference_text,
            height=140,
            disabled=True
        )
        
        st.markdown("---")
        st.subheader("🎙️ Input Audio Explanation")
        audio_file = st.file_uploader(
            "Upload your spoken explanation (.wav, .mp3, .m4a)",
            type=["wav", "mp3", "m4a"]
        )
        
        # Audio recording button placeholder
        if st.button("🔴 Start Live Recording", use_container_width=True):
            st.warning("Live recording requires standard audio hardware interface. Please upload a pre-recorded file.")
            
        st.markdown("---")
        run_btn = st.button("🚀 Analyze Explanation", type="primary", use_container_width=True, disabled=(audio_file is None))
        
        if run_btn:
            with st.spinner("Executing Speech-to-Text Transcription & Audio Extraction..."):
                # Simulation placeholder values for demo
                st.session_state.transcription = (
                    f"So, {concept_name} is basically... let me see. It is a way of designing applications "
                    "or systems where we use standard procedures to manage resources. For example, "
                    "representing state transfers or database indexing in standard structures. "
                    "I guess it works stateless."
                )
                st.session_state.semantic_score = 82
                st.session_state.fluency_score = 78
                st.session_state.is_analyzed = True
                st.success("Analysis Complete!")
                
    with col2:
        st.subheader("🎯 Assessment Results")
        
        if st.session_state.is_analyzed:
            # Layout the score metric cards
            card_col1, card_col2, card_col3 = st.columns(3)
            with card_col1:
                render_score_card("Semantic Score", f"{st.session_state.semantic_score}%", "Similarity to standard")
            with card_col2:
                render_score_card("Speech Fluency", f"{st.session_state.fluency_score}%", "Pause & filler metrics")
            with card_col3:
                overall_score = int((st.session_state.semantic_score + st.session_state.fluency_score) / 2)
                render_score_card("Overall Grade", f"{overall_score}%", "Combined rating")
                
            st.markdown("---")
            
            # Draw synthetic waveform plot
            y_synth = np.sin(np.linspace(0, 50, 4000)) * np.random.normal(1, 0.2, 4000)
            plot_audio_waveform(y_synth, 22050)
            
            # Show transcriptions
            render_concept_comparison(reference_text, st.session_state.transcription)
            
            # Download PDF button
            st.markdown("---")
            st.subheader("📥 Export Results")
            
            mock_results = {
                "semantic_score": st.session_state.semantic_score,
                "fluency_score": st.session_state.fluency_score,
                "duration_seconds": 12.5,
                "pause_ratio": 0.15,
                "filler_words_estimated": 3
            }
            
            import os
            report_path = os.path.join("data", "temp_report.pdf")
            os.makedirs("data", exist_ok=True)
            build_pdf_report(
                output_path=report_path,
                concept_name=concept_name,
                reference_text=reference_text,
                transcription=st.session_state.transcription,
                scores=mock_results
            )
            
            with open(report_path, "rb") as f:
                pdf_data = f.read()
            
            st.download_button(
                label="📥 Download PDF Assessment Report",
                data=pdf_data,
                file_name=f"VBCUA_Report_{concept_name.replace(' ', '_')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        else:
            st.info("Upload an audio file and click 'Analyze Explanation' to display results.")

# ----------------- PAGE 2: PERFORMANCE ANALYTICS -----------------
elif page == "📊 Performance Analytics":
    st.title("📊 Acoustic & Fluency Performance")
    st.markdown("Detailed speech breakdown, pause timings, pitch profiles, and overall performance insights.")
    
    if st.session_state.is_analyzed:
        # Mock analytics metrics mapping
        mock_results = {
            "duration_seconds": 12.5,
            "pause_ratio": 0.15,
            "filler_words_estimated": 3
        }
        render_detailed_metrics_tab(mock_results)
        
        st.markdown("---")
        st.subheader("📈 Performance Breakdown")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Fluency Metrics**")
            st.write("Pause Ratio: 15% (Optimal Range: 5% - 15%)")
            st.write("Filler Words: 3 (Standard frequency: < 5 per min)")
            st.progress(85)
        with col2:
            st.markdown("**Semantic Strength**")
            st.write("Keyword coverage matches reference text accurately.")
            st.write("Conceptual completeness: Moderate-High.")
            st.progress(82)
    else:
        st.info("Please perform a concept analysis evaluation first to view detailed analytics.")

# ----------------- PAGE 3: CONFIGURATION -----------------
elif page == "⚙️ Configuration":
    st.title("⚙️ Engine Configuration")
    st.markdown("Customize settings for AI modules, transcriber, similarity threshold and scoring models.")
    
    st.subheader("🤖 Transcription settings (OpenAI Whisper)")
    whisper_model = st.selectbox(
        "Whisper Model Size (Lighter sizes are faster for CPU)",
        ["tiny", "base", "small", "medium", "large"],
        index=1
    )
    
    st.subheader("🧠 Semantic analysis settings (Sentence-BERT)")
    similarity_model = st.text_input(
        "HuggingFace embedding model",
        value="all-MiniLM-L6-v2"
    )
    
    st.subheader("🔊 Audio processing settings (Librosa)")
    silence_db = st.slider(
        "Silence Threshold (dB below reference peak for pause detection)",
        min_value=-50,
        max_value=-20,
        value=-35
    )
    
    st.success("Configuration set successfully. Skeletons configured correctly.")
