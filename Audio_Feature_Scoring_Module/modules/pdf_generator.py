from __future__ import annotations
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle


def generate_pdf_report(output_path: str, data: dict) -> str:
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph("Voice-Based Concept Understanding Analyser Report", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Reference Concept", styles["Heading2"]))
    story.append(Paragraph(data.get("reference", ""), styles["BodyText"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Student Transcription", styles["Heading2"]))
    story.append(Paragraph(data.get("transcript", "") or "Transcript unavailable.", styles["BodyText"]))
    story.append(Spacer(1, 10))
    waveform = data.get("waveform_path")
    if waveform:
        story.append(Paragraph("Audio Visualization", styles["Heading2"]))
        story.append(Image(waveform, width=420, height=140))
        story.append(Spacer(1, 10))
    rows = [["Metric", "Value"]]
    for k, v in data.get("metrics", {}).items():
        rows.append([k, str(v)])
    table = Table(rows, colWidths=[230, 230])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ]))
    story.append(Paragraph("Evaluation Summary", styles["Heading2"]))
    story.append(table)
    story.append(Spacer(1, 12))
    story.append(Paragraph("AI Feedback", styles["Heading2"]))
    story.append(Paragraph(data.get("feedback", "").replace("\n", "<br/>"), styles["BodyText"]))
    doc.build(story)
    return output_path
