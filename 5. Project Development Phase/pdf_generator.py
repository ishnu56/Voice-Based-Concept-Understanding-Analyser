from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph

def generate_pdf(transcribed_text, score, level):
    filename = "reports/evaluation_report.pdf"

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    elements = []

    elements = []

    elements.append(Paragraph("<b>AI Speech Evaluation Report</b>", styles["Title"]))

    elements.append(Paragraph(f"<b>Transcribed Text:</b><br/>{transcribed_text}", styles["BodyText"]))

    elements.append(Paragraph(f"<b>Similarity Score:</b> {score:.2f}%", styles["BodyText"]))

    elements.append(Paragraph(f"<b>Understanding Level:</b> {level}", styles["BodyText"]))

    elements.append(Paragraph(f"<b>Word Count:</b> {len(transcribed_text.split())}", styles["BodyText"]))

    doc.build(elements)

    return filename