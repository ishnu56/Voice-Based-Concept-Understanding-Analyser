def evaluate_understanding(similarity: float, filler_ratio: float, audio: dict) -> dict:
    semantic_points = similarity * 55
    filler_points = 20 if filler_ratio <= 0.03 else 14 if filler_ratio <= 0.08 else 7
    pause = float(audio.get("pause_ratio", 0))
    rms = float(audio.get("rms_energy", 0))
    pause_points = 15 if pause <= 0.25 else 10 if pause <= 0.45 else 5
    energy_points = 10 if rms >= 0.01 else 5
    final = round(min(100, semantic_points + filler_points + pause_points + energy_points), 2)
    if final >= 80:
        level = "Strong Understanding"
        css_class = "success-box"
    elif final >= 50:
        level = "Moderate Understanding"
        css_class = "warning-box"
    else:
        level = "Poor Understanding"
        css_class = "danger-box"
    return {"score": final, "level": level, "css_class": css_class}
