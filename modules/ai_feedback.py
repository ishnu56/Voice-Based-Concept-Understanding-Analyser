def generate_feedback(similarity: float, filler: dict, audio: dict, result: dict) -> str:
    points = []
    if similarity >= 0.75:
        points.append("The explanation is conceptually aligned with the reference answer.")
    elif similarity >= 0.45:
        points.append("The explanation covers some important ideas but misses key conceptual points.")
    else:
        points.append("The explanation needs stronger connection to the reference concept.")

    if filler.get("filler_ratio", 0) > 0.08:
        points.append("Reduce filler words such as um, uh and like to improve fluency.")
    else:
        points.append("Filler word usage is acceptable and does not strongly affect clarity.")

    if audio.get("pause_ratio", 0) > 0.45:
        points.append("The speech contains long pauses, indicating hesitation. Practice speaking more continuously.")
    else:
        points.append("Pause level is reasonable for an explanatory speech.")

    if audio.get("rms_energy", 0) < 0.01:
        points.append("Voice energy appears low. Speak louder and closer to the microphone.")
    else:
        points.append("Voice energy indicates audible and confident delivery.")

    points.append(f"Final classification: {result.get('level', 'Not evaluated')}.")
    return "\n".join(f"• {p}" for p in points)
