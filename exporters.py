from __future__ import annotations

from typing import Any


def _join(items):
    return ", ".join(str(x) for x in (items or []) if x)


def _base_fields(data: dict) -> dict:
    instruments = data.get("instrumentation") or data.get("main_instruments") or []
    return {
        "genre": data.get("genre") or "original contemporary music",
        "subgenre": data.get("subgenre") or "",
        "bpm": data.get("bpm") or "reference-matched",
        "key": data.get("key") or "unspecified key",
        "scale": data.get("scale") or "",
        "mood": _join(data.get("mood") or []),
        "instruments": _join(instruments),
    }


def stable_audio(data: dict, duration: int = 120) -> dict[str, Any]:
    b = _base_fields(data)
    mix = data.get("mix") or {}
    master = data.get("master") or {}

    prompt = (
        f"{b['genre']}, {b['subgenre']}, {b['bpm']} BPM, {b['key']} {b['scale']}, "
        f"{b['mood']}, {b['instruments']}, original composition, "
        f"reference-informed groove and arrangement, no recognizable borrowed melody, "
        f"{mix.get('stereo_width', 'balanced stereo image')} stereo image, "
        f"{mix.get('compression', 'controlled compression')}, "
        f"{mix.get('reverb', 'controlled ambience')}, "
        f"{master.get('character', 'polished modern master')}, high fidelity"
    )
    negative = (
        "copied melody, recognizable riff, signature hook imitation, copyrighted sample, "
        "low quality, distorted audio, clipping, muddy mix, harsh highs, weak low end, "
        "unstable tempo, out of tune elements, excessive reverb"
    )
    return {
        "platform": "Stable Audio",
        "platform_url": "https://stableaudio.com/",
        "main_prompt": prompt,
        "negative_prompt": negative,
        "recommended_duration_seconds": duration,
        "platform_note": (
            "Stable Audio 3.0 is primarily aimed at instrumental generation. "
            "Use this export for the instrumental, stems, or audio-to-audio work; "
            "do not rely on it for intelligible sung lyrics."
        ),
    }


def soundraw(data: dict, duration: int = 180) -> dict[str, Any]:
    b = _base_fields(data)
    bpm = data.get("bpm")
    if isinstance(bpm, (int, float)):
        tempo = "Slow" if bpm < 100 else "Normal" if bpm <= 130 else "Fast"
    else:
        tempo = "Normal"

    structure = ((data.get("arrangement") or {}).get("structure") or
                 ["Intro", "Verse", "Chorus", "Verse", "Chorus", "Outro"])

    return {
        "platform": "SOUNDRAW",
        "platform_url": "https://soundraw.io/",
        "genre": b["genre"],
        "mood_theme": data.get("mood") or [],
        "tempo_label": tempo,
        "bpm_reference": bpm,
        "instruments_to_keep": data.get("instrumentation") or data.get("main_instruments") or [],
        "instruments_to_mute": [],
        "length_seconds": duration,
        "energy_curve": " -> ".join(structure),
        "platform_note": (
            "SOUNDRAW currently focuses on instrumental tracks and does not generate "
            "integrated sung lyrics. Generate the instrumental there and add vocals separately."
        ),
    }


def heartmula(data: dict, title: str = "") -> dict[str, Any]:
    b = _base_fields(data)
    vocal = data.get("vocal") or {}
    tags = [
        b["genre"], b["subgenre"], f"{b['bpm']} BPM",
        f"{b['key']} {b['scale']}", b["mood"], b["instruments"],
        vocal.get("style", ""), "original composition", "high fidelity"
    ]
    tags = ", ".join(x for x in tags if x)

    structure = ((data.get("arrangement") or {}).get("structure") or
                 ["Intro", "Verso 1", "Refrão", "Verso 2", "Refrão", "Ponte", "Refrão Final", "Outro"])
    lyrics = data.get("lyrics") or ""

    return {
        "platform": "HeartMuLa",
        "platform_url": "https://heartmula.github.io/",
        "style_tags": tags,
        "title": title or "Nova composição",
        "lyrics_structure": structure,
        "lyrics": lyrics,
        "platform_note": (
            "HeartMuLa supports lyrics, style tags and structured song sections, "
            "making it the best fit among these three when the final output must include vocals."
        ),
    }


def export_for_platform(platform: str, data: dict, title: str = "", duration: int = 180) -> dict:
    if platform == "stable_audio":
        return stable_audio(data, min(duration, 180))
    if platform == "soundraw":
        return soundraw(data, min(max(duration, 10), 300))
    return heartmula(data, title=title)
