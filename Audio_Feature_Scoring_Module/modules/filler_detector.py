import re

FILLER_WORDS = [
    "um", "uh", "erm", "hmm", "like", "actually", "basically",
    "literally", "you know", "i mean", "sort of", "kind of"
]


def detect_filler_words(text: str) -> dict:
    text_lower = (text or "").lower()
    total_words = len(re.findall(r"\b\w+\b", text_lower))
    counts = {}
    total_fillers = 0
    for filler in FILLER_WORDS:
        pattern = r"\b" + re.escape(filler) + r"\b"
        count = len(re.findall(pattern, text_lower))
        if count:
            counts[filler] = count
            total_fillers += count
    ratio = total_fillers / total_words if total_words else 0.0
    return {
        "counts": counts,
        "total_fillers": total_fillers,
        "total_words": total_words,
        "filler_ratio": round(ratio, 4),
    }
