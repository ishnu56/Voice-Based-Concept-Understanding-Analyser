def compare_words(reference, spoken):
    ref_words = reference.lower().split()
    spoken_words = spoken.lower().split()

    matched = []
    missing = []
    extra = []

    for word in ref_words:
        if word in spoken_words:
            matched.append(word)
        else:
            missing.append(word)

    for word in spoken_words:
        if word not in ref_words:
            extra.append(word)

    return matched, missing, extra