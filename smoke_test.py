from heuristic_engine import build_analysis
from exporters import export_for_platform, export_json_for_platform, SUNO_JSON_MAX_CHARS

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

for platform in ("stable_audio", "soundraw", "heartmula", "suno"):
    exported = export_for_platform(platform, analysis, title="Faixa Teste", duration=180)
    assert exported["platform"]
    assert exported["platform_url"]

suno_export = export_for_platform("suno", analysis, title="Faixa Teste", duration=180)
assert suno_export["platform"] == "Suno"
assert suno_export["mode"] == "Custom"
assert suno_export["lyrics"] == "Minha letra de teste."
assert suno_export["title"] == "Faixa Teste"
assert "styles" in suno_export
assert "exclude" in suno_export

suno_json = export_json_for_platform("suno", suno_export)
assert len(suno_json) <= SUNO_JSON_MAX_CHARS

long_analysis = dict(analysis)
long_analysis["lyrics"] = "Verso em português com acentuação. " * 300
long_suno_export = export_for_platform("suno", long_analysis, title="Faixa Longa", duration=240)
long_suno_json = export_json_for_platform("suno", long_suno_export)
assert len(long_suno_json) <= SUNO_JSON_MAX_CHARS
assert len(long_suno_export["lyrics"]) > SUNO_JSON_MAX_CHARS

print("SMOKE_TEST_OK")
