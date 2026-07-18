from __future__ import annotations
import math
from collections import Counter
import streamlit as st


def _tokenize(text: str) -> list[str]:
    return [w.strip(".,!?;:()[]{}\"'").lower() for w in text.split() if w.strip()]


def _cosine_from_counters(a: Counter, b: Counter) -> float:
    words = set(a) | set(b)
    dot = sum(a[w] * b[w] for w in words)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def semantic_similarity(student_text: str, reference_text: str) -> float:
    """Return semantic similarity between 0 and 1.

    Uses Sentence-BERT when installed. Falls back to lexical cosine similarity
    so the project remains runnable on low-spec college systems.
    """
    student_text = student_text or ""
    reference_text = reference_text or ""
    try:
        from sentence_transformers import util

        model = load_sentence_model()
        embeddings = model.encode([student_text, reference_text], convert_to_tensor=True)
        score = util.cos_sim(embeddings[0], embeddings[1]).item()
        return round(max(0.0, min(1.0, float(score))), 4)
    except Exception:
        score = _cosine_from_counters(Counter(_tokenize(student_text)), Counter(_tokenize(reference_text)))
        return round(max(0.0, min(1.0, score)), 4)


@st.cache_resource(show_spinner=False)
def load_sentence_model():
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer("all-MiniLM-L6-v2")
