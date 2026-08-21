from __future__ import annotations

import json
import os
import uuid
from pathlib import Path

from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename

from audio_analysis import analyze_audio
from reference_metadata import youtube_metadata
from heuristic_engine import build_analysis
from ai_engine import enrich_with_ai
from exporters import export_for_platform, export_json_for_platform


BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
EXPORT_DIR = BASE_DIR / "exports"
UPLOAD_DIR.mkdir(exist_ok=True)
EXPORT_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".mp3", ".wav", ".flac", ".m4a", ".ogg", ".aac"}

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 35 * 1024 * 1024
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-change-me")


def allowed_file(filename: str) -> bool:
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS


def configured_ai_provider() -> str:
    return os.getenv("AI_PROVIDER", "none").strip().lower()


def ai_provider_label(provider: str) -> str:
    labels = {
        "ollama": "Ollama",
        "openai_compatible": "LM Studio / OpenAI-compatible",
    }
    return labels.get(provider, "Não configurada")


@app.get("/")
def index():
    provider = configured_ai_provider()
    return render_template(
        "index.html",
        provider=provider,
        provider_label=ai_provider_label(provider),
        ai_available=provider not in {"", "none", "off"},
    )


@app.post("/analyze")
def analyze():
    reference_input = (request.form.get("reference") or "").strip()
    lyrics = (request.form.get("lyrics") or "").strip()
    schema = (request.form.get("schema") or "B").upper()
    platform = (request.form.get("platform") or "heartmula").strip()
    target_title = (request.form.get("target_title") or "").strip()
    duration = int(request.form.get("duration") or 180)
    use_ai = (request.form.get("use_ai") or "").strip() == "1"
    provider = configured_ai_provider()
    ai_available = provider not in {"", "none", "off"}

    if not reference_input:
        return render_template("error.html", message="Informe uma música de referência por link ou título/artista."), 400

    reference = youtube_metadata(reference_input)
    audio_features = None
    audio_warning = None

    upload = request.files.get("audio_file")
    uploaded_path = None

    if upload and upload.filename:
        if not allowed_file(upload.filename):
            return render_template("error.html", message="Formato de áudio não suportado."), 400

        suffix = Path(upload.filename).suffix.lower()
        uploaded_path = UPLOAD_DIR / f"{uuid.uuid4().hex}{suffix}"
        upload.save(uploaded_path)

        try:
            audio_features = analyze_audio(str(uploaded_path))
        except Exception as exc:
            audio_warning = f"Não foi possível extrair os parâmetros do áudio enviado: {exc}"

    base = build_analysis(reference, lyrics, schema, audio_features)

    if use_ai and ai_available:
        analysis_data, ai_warning = enrich_with_ai(
            base, reference, audio_features, schema, enabled=True
        )
    elif use_ai and not ai_available:
        analysis_data = base
        ai_warning = (
            "A IA complementar foi solicitada, mas nenhum provedor está configurado. "
            "A análise continuou apenas com o motor acústico e heurístico local."
        )
    else:
        analysis_data = base
        ai_warning = None

    export = export_for_platform(platform, analysis_data, target_title, duration)
    export_json = export_json_for_platform(platform, export)

    result_id = uuid.uuid4().hex
    result_payload = {
        "reference": reference,
        "audio_features": audio_features,
        "analysis": analysis_data,
        "ai": {
            "requested": use_ai,
            "available": ai_available,
            "provider": provider if ai_available else "none",
            "provider_label": ai_provider_label(provider),
        },
        "export": export,
    }
    json_path = EXPORT_DIR / f"{result_id}.json"
    json_path.write_text(json.dumps(result_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    return render_template(
        "result.html",
        reference=reference,
        audio=audio_features,
        analysis=analysis_data,
        export=export,
        analysis_json=json.dumps(analysis_data, ensure_ascii=False, indent=2),
        export_json=export_json,
        export_json_length=len(export_json),
        result_id=result_id,
        warning=ai_warning or audio_warning,
        ai_requested=use_ai,
        ai_available=ai_available,
        ai_provider_label=ai_provider_label(provider),
    )


@app.get("/download/<result_id>")
def download(result_id: str):
    if not result_id.isalnum():
        return "Identificador inválido", 400
    path = EXPORT_DIR / f"{result_id}.json"
    if not path.exists():
        return "Arquivo não encontrado", 404
    return send_file(path, as_attachment=True, download_name="music_reference_analysis.json")


@app.errorhandler(413)
def too_large(_):
    return render_template("error.html", message="O arquivo excede o limite de 35 MB."), 413


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
