from __future__ import annotations

import pandas as pd
import streamlit as st


def render_concept_comparison(reference_text: str, transcription: str) -> None:
    st.subheader("Concept Comparison")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Reference Concept**")
        st.info(reference_text)
    with col2:
        st.markdown("**Student Explanation**")
        st.write(transcription)


def render_detailed_metrics_tab(metrics: dict) -> None:
    st.subheader("Detailed Metrics")
    rows = [{"Metric": key.replace("_", " ").title(), "Value": value} for key, value in metrics.items()]
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
