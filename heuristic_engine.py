from __future__ import annotations

from copy import deepcopy
from typing import Any

from schemas import COMPACT_TEMPLATE, ADVANCED_TEMPLATE


def _guess_mood(audio: dict | None) -> list[str]:
    if not audio:
        return ["focused", "contemporary"]

    mood = []
    if audio.get("scale_estimated") == "minor":
        mood += ["moody", "emotional"]
    else:
        mood += ["uplifting", "open"]

    bpm = audio.get("bpm_estimated") or 110
    if bpm >= 130:
        mood.append("energetic")
    elif bpm < 90:
        mood.append("introspective")
    else:
        mood.append("driving")

    if audio.get("brightness") == "dark":
        mood.append("dark")
    elif audio.get("brightness") == "bright":
        mood.append("bright")

    return list(dict.fromkeys(mood))


def _default_structure(duration: float | None) -> list[str]:
    if not duration:
        return ["Intro", "Verse", "Chorus", "Verse", "Chorus", "Bridge", "Final Chorus", "Outro"]
    if duration < 75:
        return ["Intro", "Verse", "Chorus", "Outro"]
    if duration < 150:
        return ["Intro", "Verse", "Chorus", "Verse", "Chorus", "Outro"]
    return ["Intro", "Verse", "Pre-Chorus", "Chorus", "Verse", "Pre-Chorus", "Chorus", "Bridge", "Final Chorus", "Outro"]


def build_analysis(reference: dict, lyrics: str, schema: str, audio: dict | None) -> dict[str, Any]:
    is_advanced = schema == "B"
    out = deepcopy(ADVANCED_TEMPLATE if is_advanced else COMPACT_TEMPLATE)

    out["reference"] = reference
    out["lyrics"] = lyrics or ""
    out["bpm"] = audio.get("bpm_estimated") if audio else None
    out["key"] = audio.get("key_estimated", "") if audio else ""
    out["scale"] = audio.get("scale_estimated", "") if audio else ""
    out["mood"] = _guess_mood(audio)

    title = (reference.get("title") or reference.get("reference") or "").lower()

    genre_map = {
        "rock": ("Rock", "Alternative Rock"),
        "metal": ("Metal", "Modern Metal"),
        "trap": ("Hip Hop", "Trap"),
        "drill": ("Hip Hop", "Drill"),
        "house": ("Electronic", "House"),
        "techno": ("Electronic", "Techno"),
        "synthwave": ("Electronic", "Synthwave"),
        "lofi": ("Hip Hop", "Lo-Fi Hip Hop"),
        "lo-fi": ("Hip Hop", "Lo-Fi Hip Hop"),
        "pop": ("Pop", "Contemporary Pop"),
        "funk": ("Funk", "Modern Funk"),
        "jazz": ("Jazz", "Contemporary Jazz"),
        "ambient": ("Ambient", "Cinematic Ambient"),
        "cinematic": ("Cinematic", "Hybrid Cinematic"),
        "reggaeton": ("Latin", "Reggaeton"),
        "afrobeat": ("Afrobeats", "Afrobeats"),
        "phonk": ("Electronic", "Phonk"),
        "country": ("Country", "Contemporary Country"),
    }

    genre, subgenre = ("Reference-driven", "Original derivative style")
    for token, pair in genre_map.items():
        if token in title:
            genre, subgenre = pair
            break

    out["genre"] = genre
    out["subgenre"] = subgenre

    instruments = ["drums", "bass", "harmonic accompaniment", "lead texture"]
    if "rock" in title or "metal" in title:
        instruments = ["electric guitar", "bass guitar", "acoustic drums", "lead guitar texture"]
    elif any(x in title for x in ["house", "techno", "synthwave", "electronic", "phonk"]):
        instruments = ["drum machine", "synth bass", "synthesizer", "atmospheric pads"]
    elif any(x in title for x in ["trap", "drill", "hip hop", "lofi", "lo-fi"]):
        instruments = ["808 bass", "drum machine", "hi-hats", "sample-like harmonic texture"]

    if is_advanced:
        out["instrumentation"] = instruments
        structure = _default_structure(audio.get("duration_seconds") if audio else None)
        out["arrangement"]["structure"] = structure
        out["arrangement"]["section_notes"] = {
            section: (
                "low density" if section == "Intro"
                else "reduced arrangement" if "Verse" in section
                else "highest density and hook focus" if "Chorus" in section
                else "contrast section" if section == "Bridge"
                else "decompression and tail"
            )
            for section in structure
        }
        out["energy_curve"] = [
            {"section": section, "energy": (
                25 if section == "Intro"
                else 55 if "Verse" in section
                else 70 if "Pre-Chorus" in section
                else 88 if "Chorus" in section
                else 60 if section == "Bridge"
                else 30
            )}
            for section in structure
        ]
        if audio:
            out["drums"]["density"] = audio.get("rhythmic_density", "")
            out["drums"]["character"] = "punchy" if (audio.get("percussion_ratio") or 0) > 0.45 else "balanced"
            out["drums"]["groove"] = f"{audio.get('tempo_band', 'medium')} tempo groove"
            out["mix"]["brightness"] = audio.get("brightness", "")
            out["mix"]["dynamic_profile"] = audio.get("dynamic_profile", "")
            width = (audio.get("stereo") or {}).get("width_score")
            out["mix"]["stereo_width"] = (
                "wide" if width is not None and width > 0.55
                else "moderate" if width is not None and width > 0.25
                else "focused"
            )
        else:
            out["drums"]["density"] = "moderate"
            out["drums"]["character"] = "controlled"
            out["drums"]["groove"] = "reference-driven groove"
            out["mix"]["brightness"] = "balanced"
            out["mix"]["dynamic_profile"] = "moderate"
            out["mix"]["stereo_width"] = "moderate"

        out["bass"] = {"character": "defined low end", "movement": "supports the groove without copying a signature bassline"}
        out["harmony"] = {"character": "reference-compatible harmonic language", "harmonic_rhythm": "moderate"}
        out["vocal"] = {
            "presence": "lead vocal if lyrics are provided",
            "style": "emotionally aligned with the reference",
            "gender_timbre": "unspecified",
            "delivery": "clear, natural phrasing",
            "processing": ["controlled compression", "short ambience", "light saturation"]
        }
        out["mix"]["reverb"] = "controlled, section-dependent"
        out["mix"]["compression"] = "modern controlled compression"
        out["mix"]["density"] = "builds toward chorus"
        out["master"] = {"character": "polished modern master", "quality": "high fidelity"}
        out["transitions"] = ["risers or fills where appropriate", "contrast before chorus", "clean outro"]
        out["production_tags"] = [
            "original composition", "reference-informed", "high fidelity",
            "no copied melody", "no recognizable riff", "no copyrighted samples"
        ]
    else:
        out["main_instruments"] = instruments
        out["vocal"] = {
            "presence": "lead vocal if lyrics are provided",
            "style": "reference-compatible but original",
            "gender_timbre": "unspecified",
            "delivery": "clear and expressive"
        }
        out["production_tags"] = [
            "original composition", "reference-informed", "high fidelity",
            "no copied melody", "no recognizable riff"
        ]

    return out
