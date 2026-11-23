#!/usr/bin/env bash
# Roda os testes internos de um cenário contra V_fix e V_bug.
# Uso: ./cenarios/rodar_testes.sh C1
# Esperado: V_fix "TODOS PASSARAM"; V_bug falha só nos testes [GATILHO Dn].
set -euo pipefail
cenario="${1:?informe o cenário, ex.: C1}"
dir="$(cd "$(dirname "$0")/$cenario" && pwd)"
teste="$(ls "$dir"/testes/*.java)"
classe_teste="$(basename "$teste" .java)"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
for versao in V_fix V_bug; do
    echo "== $cenario $versao"
    mkdir -p "$tmp/$versao"
    javac -encoding UTF-8 -d "$tmp/$versao" "$dir/$versao"/*.java "$teste"
    java -cp "$tmp/$versao" "$classe_teste" || true
done
