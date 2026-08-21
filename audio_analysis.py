from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import librosa
import numpy as np


NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# Perfis de Krumhansl simplificados.
MAJOR_PROFILE = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
MINOR_PROFILE = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])


def _corr(a: np.ndarray, b: np.ndarray) -> float:
    if np.std(a) == 0 or np.std(b) == 0:
        return 0.0
    return float(np.corrcoef(a, b)[0, 1])


def estimate_key(chroma_mean: np.ndarray) -> tuple[str, str, float]:
    best = ("C", "major", -999.0)
    for root in range(12):
        major = np.roll(MAJOR_PROFILE, root)
        minor = np.roll(MINOR_PROFILE, root)
        cmaj = _corr(chroma_mean, major)
        cmin = _corr(chroma_mean, minor)
        if cmaj > best[2]:
            best = (NOTE_NAMES[root], "major", cmaj)
        if cmin > best[2]:
            best = (NOTE_NAMES[root], "minor", cmin)
    return best


def _safe_db(x: np.ndarray) -> np.ndarray:
    return librosa.amplitude_to_db(np.maximum(x, 1e-10), ref=1.0)


def _stereo_width(path: str) -> dict[str, Any]:
    y, sr = librosa.load(path, sr=22050, mono=False, duration=180)
    if y.ndim != 2 or y.shape[0] < 2:
        return {"stereo": False, "correlation": None, "width_score": None}
    left, right = y[0], y[1]
    n = min(len(left), len(right))
    if n < 100:
        return {"stereo": True, "correlation": None, "width_score": None}
    corr = float(np.corrcoef(left[:n], right[:n])[0, 1])
    width_score = float(np.clip(1.0 - abs(corr), 0.0, 1.0))
    return {
        "stereo": True,
        "correlation": round(corr, 3),
        "width_score": round(width_score, 3),
    }


def analyze_audio(path: str) -> dict[str, Any]:
    path_obj = Path(path)
    y, sr = librosa.load(path, sr=22050, mono=True, duration=240)

    if y.size < sr:
        raise ValueError("O arquivo de áudio é curto demais para análise.")

    duration = float(librosa.get_duration(y=y, sr=sr))

    tempo_arr = librosa.feature.tempo(y=y, sr=sr, aggregate=np.median)
    tempo = float(np.atleast_1d(tempo_arr)[0])

    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    chroma_mean = chroma.mean(axis=1)
    key, mode, confidence = estimate_key(chroma_mean)

    rms = librosa.feature.rms(y=y)[0]
    rms_db = _safe_db(rms)
    loudness_db = float(np.median(rms_db))
    dynamic_range = float(np.percentile(rms_db, 95) - np.percentile(rms_db, 10))

    centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    centroid_hz = float(np.median(centroid))

    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    onset_frames = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr)
    onset_density = float(len(onset_frames) / max(duration, 1.0))

    harmonic, percussive = librosa.effects.hpss(y)
    harm_rms = float(np.sqrt(np.mean(harmonic ** 2)) + 1e-12)
    perc_rms = float(np.sqrt(np.mean(percussive ** 2)) + 1e-12)
    percussion_ratio = float(perc_rms / (harm_rms + perc_rms))

    zcr = librosa.feature.zero_crossing_rate(y)[0]
    zero_crossing_rate = float(np.median(zcr))

    stereo = _stereo_width(path)

    tempo_band = (
        "slow" if tempo < 90
        else "medium" if tempo <= 130
        else "fast"
    )

    brightness = (
        "dark" if centroid_hz < 1700
        else "balanced" if centroid_hz < 3000
        else "bright"
    )

    dynamics = (
        "compressed" if dynamic_range < 9
        else "moderate" if dynamic_range < 16
        else "wide"
    )

    rhythmic_density = (
        "sparse" if onset_density < 1.4
        else "moderate" if onset_density < 2.8
        else "dense"
    )

    return {
        "file_name": path_obj.name,
        "duration_seconds": round(duration, 2),
        "bpm_estimated": round(tempo, 1),
        "tempo_band": tempo_band,
        "key_estimated": key,
        "scale_estimated": mode,
        "key_confidence": round(confidence, 3),
        "loudness_rms_db": round(loudness_db, 1),
        "dynamic_range_db": round(dynamic_range, 1),
        "dynamic_profile": dynamics,
        "spectral_centroid_hz": round(centroid_hz, 0),
        "brightness": brightness,
        "onset_density_per_second": round(onset_density, 2),
        "rhythmic_density": rhythmic_density,
        "percussion_ratio": round(percussion_ratio, 3),
        "zero_crossing_rate": round(zero_crossing_rate, 4),
        "stereo": stereo,
        "analysis_note": "Valores acústicos são estimativas e devem ser tratados como referência, não como transcrição exata."
    }
