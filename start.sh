#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker não encontrado."
  exit 1
fi

if [ ! -f .env ]; then
  cp .env.example .env
  echo ".env criado a partir de .env.example"
fi

docker compose up -d --build

echo
echo "Music Reference Lab iniciado."
echo "Abra: http://localhost:8080"
