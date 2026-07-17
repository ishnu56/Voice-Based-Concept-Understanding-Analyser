from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_certificate(score, grammar_score, rating, level):

    pdf_path = "certificate.pdf"

    doc = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b><font size=20>Certificate of Performance</font></b>", styles["Title"]))

    story.append(Paragraph("<br/><br/>This certificate is proudly awarded for successfully completing the AI Speech Evaluation.", styles["BodyText"]))

    story.append(Paragraph(f"<br/><b>Overall Score:</b> {score:.2f}%", styles["BodyText"]))
    story.append(Paragraph(f"<b>Grammar Score:</b> {grammar_score:.2f}%", styles["BodyText"]))
    story.append(Paragraph(f"<b>Rating:</b> {rating}/5", styles["BodyText"]))
    story.append(Paragraph(f"<b>Understanding Level:</b> {level}", styles["BodyText"]))

    story.append(Paragraph("<br/><br/><b>Congratulations!</b>", styles["Title"]))

    doc.build(story)

    return pdf_path