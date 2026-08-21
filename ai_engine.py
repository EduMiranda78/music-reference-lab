from __future__ import annotations

import json
import os
import re

import requests


SYSTEM_PROMPT = """
You are a senior music-production analyst.

Analyze a music reference only at the level of general musical and production characteristics.
The goal is to design a NEW and ORIGINAL composition.

Allowed to preserve as reference:
genre, subgenre, approximate BPM, key/scale, mood, groove family, instrumentation,
arrangement archetype, energy curve, drum character, bass character, vocal profile,
mixing character, mastering character and general production texture.

Do not reproduce or request:
a recognizable melody, signature riff, signature hook, copyrighted lyrics, samples,
distinctive instrumental phrases, or a close reconstruction of a specific recording.

All technical JSON values must be in English.
The field "lyrics" must remain exactly in Portuguese as supplied by the user.
Return valid JSON only, with no markdown fences.
"""


def _extract_json(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.I)
        text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except Exception:
        m = re.search(r"\{.*\}", text, flags=re.S)
        if not m:
            raise
        return json.loads(m.group(0))


def _build_user_prompt(base_analysis: dict, reference: dict, audio: dict | None, schema: str) -> str:
    return f"""
Reference metadata:
{json.dumps(reference, ensure_ascii=False, indent=2)}

Measured acoustic features, when available:
{json.dumps(audio or {}, ensure_ascii=False, indent=2)}

Required schema:
{json.dumps(base_analysis, ensure_ascii=False, indent=2)}

Schema mode: {"advanced" if schema == "B" else "compact"}.

Improve and complete the supplied JSON conservatively.
If the reference is only a title/artist and you are not confident about a fact, keep the field general rather than inventing precision.
Never alter the Portuguese content in the lyrics field.
Return the complete JSON object.
"""


def _ollama(base_analysis: dict, reference: dict, audio: dict | None, schema: str) -> dict:
    base_url = os.getenv("OLLAMA_URL", "http://host.docker.internal:11434").rstrip("/")
    model = os.getenv("OLLAMA_MODEL", "").strip()
    if not model:
        tags = requests.get(f"{base_url}/api/tags", timeout=8).json()
        models = tags.get("models") or []
        if not models:
            raise RuntimeError("Nenhum modelo Ollama encontrado.")
        model = models[0].get("name")

    payload = {
        "model": model,
        "stream": False,
        "format": "json",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": _build_user_prompt(base_analysis, reference, audio, schema)},
        ],
        "options": {"temperature": 0.25}
    }
    r = requests.post(f"{base_url}/api/chat", json=payload, timeout=120)
    r.raise_for_status()
    return _extract_json(r.json()["message"]["content"])


def _openai_compatible(base_analysis: dict, reference: dict, audio: dict | None, schema: str) -> dict:
    base_url = os.getenv("OPENAI_COMPATIBLE_BASE_URL", "").rstrip("/")
    api_key = os.getenv("OPENAI_COMPATIBLE_API_KEY", "")
    model = os.getenv("OPENAI_COMPATIBLE_MODEL", "").strip()
    if not base_url or not model:
        raise RuntimeError("OPENAI_COMPATIBLE_BASE_URL e OPENAI_COMPATIBLE_MODEL precisam estar configurados.")

    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    payload = {
        "model": model,
        "temperature": 0.25,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": _build_user_prompt(base_analysis, reference, audio, schema)},
        ],
    }
    r = requests.post(f"{base_url}/chat/completions", headers=headers, json=payload, timeout=120)
    r.raise_for_status()
    content = r.json()["choices"][0]["message"]["content"]
    return _extract_json(content)


def enrich_with_ai(
    base_analysis: dict,
    reference: dict,
    audio: dict | None,
    schema: str,
    enabled: bool = False,
) -> tuple[dict, str | None]:
    if not enabled:
        return base_analysis, None

    provider = os.getenv("AI_PROVIDER", "none").strip().lower()
    if provider in {"", "none", "off"}:
        return base_analysis, "Nenhum provedor de IA complementar está configurado."

    try:
        if provider == "ollama":
            return _ollama(base_analysis, reference, audio, schema), None
        if provider == "openai_compatible":
            return _openai_compatible(base_analysis, reference, audio, schema), None
        return base_analysis, f"AI_PROVIDER desconhecido: {provider}"
    except Exception as exc:
        return base_analysis, f"A análise acústica foi concluída, mas a camada de IA falhou: {exc}"
