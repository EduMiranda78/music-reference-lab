from heuristic_engine import build_analysis
from exporters import export_for_platform, export_json_for_platform, SUNO_JSON_MAX_CHARS
from presets_exporter import ActionHeuristicMapper, CustomGenerator, HighEnergyPresets

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

# Presets de alta energia
assert set(HighEnergyPresets.PRESETS) == {
    "guerra_de_cria",
    "acao_epica",
    "cyberpunk_guerra",
    "tensa_perseguicao",
}

metrics = {
    "bpm": 138.0,
    "onset_density": 0.9,
    "percussion_ratio": 0.72,
    "rms": 0.18,
    "spectral_centroid": 2850.0,
    "stereo_width": 0.68,
}
action_tags = ActionHeuristicMapper(metrics).map_to_action_tags()
assert "fast-paced" in action_tags
assert "rapid-fire beats" in action_tags
assert "heavy percussion-driven" in action_tags

preset_suno = CustomGenerator.generate_suno_export(
    lyrics_pt="Verso um.\n\nRefrão forte.",
    title="Teste de Guerra",
    preset_key="guerra_de_cria",
    heuristic_tags=action_tags,
    vocal_gender="male",
)
assert preset_suno["Title"].endswith("(War Mix)")
assert "acoustic guitar" in preset_suno["Exclude"]
assert "sotaque carioca" in preset_suno["Lyrics"].lower()
assert len(preset_suno["Styles"]) <= 120

# Normaliza o payload temático para o mesmo contrato usado pelo exportador JSON do Suno.
normalized_preset_suno = {
    "platform": "Suno",
    "platform_url": "https://suno.com/create",
    "mode": "Custom",
    "title": preset_suno["Title"],
    "styles": preset_suno["Styles"],
    "lyrics": preset_suno["Lyrics"],
    "exclude": preset_suno["Exclude"],
    "creative_sliders": {
        "weirdness_percent": preset_suno["Weirdness"],
        "style_influence_percent": preset_suno["StyleInfluence"],
        "audio_influence_percent_if_uploading_audio": preset_suno["AudioInfluence"],
    },
}
assert len(export_json_for_platform("suno", normalized_preset_suno)) <= SUNO_JSON_MAX_CHARS

preset_heartmula = CustomGenerator.generate_heartmula_export(
    lyrics_pt="Verso um.\n\nRefrão forte.",
    title="Teste de Guerra",
    preset_key="acao_epica",
    heuristic_tags=action_tags,
    vocal_gender="female",
)
assert "female" in preset_heartmula["style_tags"].lower()
assert "negative_prompts" in preset_heartmula

print("SMOKE_TEST_OK")
