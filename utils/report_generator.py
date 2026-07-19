from __future__ import annotations

from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def build_pdf_report(
    output_path: str,
    concept_name: str,
    reference_text: str,
    transcription: str,
    scores: dict,
) -> str:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    pdf = canvas.Canvas(str(path), pagesize=letter)
    width, height = letter
    y = height - 50

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, y, "Voice-Based Concept Understanding Analyser")
    y -= 32

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, f"Concept: {concept_name}")
    y -= 24

    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(50, y, "Scores")
    y -= 18
    pdf.setFont("Helvetica", 10)
    for key, value in scores.items():
        pdf.drawString(60, y, f"{key.replace('_', ' ').title()}: {value}")
        y -= 15

    y -= 10
    y = _draw_wrapped(pdf, "Reference Concept", reference_text, 50, y, width - 100)
    y -= 10
    _draw_wrapped(pdf, "Student Transcription", transcription, 50, y, width - 100)

    pdf.save()
    return str(path)


def _draw_wrapped(pdf: canvas.Canvas, title: str, text: str, x: int, y: int, max_width: int) -> int:
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(x, y, title)
    y -= 16
    pdf.setFont("Helvetica", 10)
    words = (text or "").split()
    line = ""
    for word in words:
        trial = f"{line} {word}".strip()
        if pdf.stringWidth(trial, "Helvetica", 10) <= max_width:
            line = trial
        else:
            pdf.drawString(x, y, line)
            y -= 14
            line = word
    if line:
        pdf.drawString(x, y, line)
        y -= 14
    return y
