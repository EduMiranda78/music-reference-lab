from heuristic_engine import build_analysis
from exporters import export_for_platform

reference = {
    "source_type": "title_or_artist",
    "reference": "Test Rock Reference - Example Artist",
    "title": "Test Rock Reference",
    "author_name": "Example Artist",
    "url": None,
}

audio = {
    "duration_seconds": 180.0,
    "bpm_estimated": 118.0,
    "tempo_band": "medium",
    "key_estimated": "D",
    "scale_estimated": "minor",
    "brightness": "balanced",
    "dynamic_profile": "moderate",
    "rhythmic_density": "moderate",
    "percussion_ratio": 0.51,
    "stereo": {"width_score": 0.42},
}

analysis = build_analysis(
    reference=reference,
    lyrics="Minha letra de teste.",
    schema="B",
    audio=audio,
)

assert analysis["bpm"] == 118.0
assert analysis["key"] == "D"
assert analysis["scale"] == "minor"
assert analysis["lyrics"] == "Minha letra de teste."
assert analysis["genre"] == "Rock"

for platform in ("stable_audio", "soundraw", "heartmula"):
    exported = export_for_platform(platform, analysis, title="Faixa Teste", duration=180)
    assert exported["platform"]

print("SMOKE_TEST_OK")
