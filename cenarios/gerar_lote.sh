#!/usr/bin/env bash
# Gera todas as sugestões de um ou mais cenários com o gpt-oss-120b (Groq).
# Uso: GROQ_API_KEY=... ./cenarios/gerar_lote.sh C1 C2
#
# Para cada cenário, grava em cenarios/<C>/sugestoes/:
#   restrito/  prompt restrito (prompt_sistema.txt): 5x em V_bug (medidas brutas, VP das listas)
#              e 5x em V_fix (medidas brutas)
#   generico/  prompt genérico (prompt_generico.txt): 5x em V_fix (fonte do FP das listas)
# Já existentes não são refeitos. Cada execução usa ~3-5 mil tokens; a cota gratuita é de 200 mil por dia.
set -euo pipefail
raiz="$(cd "$(dirname "$0")/.." && pwd)"
if [ -z "${GROQ_API_KEY:-}" ] && [ -f "$raiz/.env" ]; then
    set -a
    # shellcheck disable=SC1090
    . "$raiz/.env"
    set +a
fi
gerar="$raiz/piloto/unidades/gerar_sugestoes.py"
for c in "$@"; do
    dir="$raiz/cenarios/$c"
    mkdir -p "$dir/sugestoes"
    cd "$dir/sugestoes"
    for spec in "restrito:prompt_sistema.txt:${c}_numerado" \
                "restrito:prompt_sistema.txt:${c}_fix_numerado" \
                "generico:prompt_generico.txt:${c}_fix_numerado"; do
        IFS=: read -r saida prompt unidade <<< "$spec"
        for n in 1 2 3 4 5; do
            [ -s "$saida/${unidade}_exec${n}.txt" ] && continue
            python3 "$gerar" "../${unidade}.txt" --execucoes 1 --inicio "$n" \
                --prompt "$raiz/cenarios/$prompt" --saida "$saida"
        done
    done
done
