from __future__ import annotations
import os
import numpy as np


def extract_audio_features(audio_path: str) -> dict:
    """Extract duration, RMS energy, pause ratio and sample rate using Librosa."""
    if not os.path.exists(audio_path):
        raise FileNotFoundError(audio_path)
    try:
        import librosa
        y, sr = librosa.load(audio_path, sr=None, mono=True)
        duration = float(librosa.get_duration(y=y, sr=sr))
        rms = librosa.feature.rms(y=y)[0]
        zcr = librosa.feature.zero_crossing_rate(y)[0]
        rms_energy = float(np.mean(rms)) if len(rms) else 0.0
        zero_crossing_rate = float(np.mean(zcr)) if len(zcr) else 0.0
        threshold = max(0.005, rms_energy * 0.35)
        pause_frames = int(np.sum(rms < threshold))
        pause_ratio = pause_frames / len(rms) if len(rms) else 0.0
        return {
            "duration": round(duration, 2),
            "sample_rate": int(sr),
            "rms_energy": round(rms_energy, 4),
            "pause_ratio": round(float(pause_ratio), 4),
            "zero_crossing_rate": round(zero_crossing_rate, 4),
        }
    except Exception as exc:
        return {
            "duration": 0.0,
            "sample_rate": 0,
            "rms_energy": 0.0,
            "pause_ratio": 0.0,
            "zero_crossing_rate": 0.0,
            "error": str(exc),
        }


def save_waveform(audio_path: str, output_path: str) -> str:
    import matplotlib.pyplot as plt
    try:
        import librosa
        y, sr = librosa.load(audio_path, sr=None, mono=True)
        time_axis = np.linspace(0, len(y) / sr, num=len(y)) if sr else np.arange(len(y))
    except Exception:
        y = np.zeros(100)
        time_axis = np.arange(100)

    plt.figure(figsize=(10, 3))
    plt.plot(time_axis, y)
    plt.title("Audio Waveform")
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    return output_path
