from __future__ import annotations

import matplotlib.pyplot as plt
import streamlit as st


def inject_premium_styles() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background: #f8fafc;
            color: #0f172a;
        }
        .metric-card {
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 16px;
            background: #ffffff;
            box-shadow: 0 1px 3px rgba(15, 23, 42, 0.08);
        }
        .metric-card h4 {
            margin: 0 0 8px;
            color: #475569;
            font-size: 0.95rem;
        }
        .metric-card .score {
            font-size: 1.8rem;
            font-weight: 800;
            color: #2563eb;
        }
        .metric-card p {
            color: #64748b;
            margin: 8px 0 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_score_card(title: str, value: str, caption: str) -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <h4>{title}</h4>
            <div class="score">{value}</div>
            <p>{caption}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def plot_audio_waveform(samples, sample_rate: int) -> None:
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(samples, linewidth=0.8, color="#2563eb")
    ax.set_title("Audio Waveform")
    ax.set_xlabel(f"Samples at {sample_rate} Hz")
    ax.set_ylabel("Amplitude")
    ax.grid(alpha=0.2)
    st.pyplot(fig)
    plt.close(fig)
