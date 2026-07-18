def highlight_text(reference, spoken):
    ref_words = reference.split()
    spoken_words = spoken.split()

    highlighted = ""

    for word in spoken_words:
        if word.lower() in [w.lower() for w in ref_words]:
            highlighted += f"<span style='color:green;font-weight:bold'>{word}</span> "
        else:
            highlighted += f"<span style='color:red;font-weight:bold'>{word}</span> "

    return highlighted