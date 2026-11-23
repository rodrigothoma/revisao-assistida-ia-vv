"""Soma os tokens das respostas do gpt-oss-120b (Groq) e estima o custo.

Uso:
    python3 custo_gemini.py cenarios            # procura todos os .json de respostas abaixo da pasta
    python3 custo_gemini.py cenarios 0.15 0.60  # preços por milhão de tokens (entrada, saída)

Preços padrão: os do gpt-oss-120b no Groq (US$ 0,15 entrada / US$ 0,60 saída por milhão).
O nome do arquivo foi mantido por compatibilidade com o piloto 1, que usou o Gemini.
"""
import json
import pathlib
import sys

pasta = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
preco_entrada = float(sys.argv[2]) if len(sys.argv) > 2 else 0.15
preco_saida = float(sys.argv[3]) if len(sys.argv) > 3 else 0.60

ent = sai = rac = n = 0
for f in pasta.rglob("*_exec*.json"):
    dados = json.loads(f.read_text(encoding="utf-8"))
    uso = dados.get("uso") or {}
    if "prompt_tokens" not in uso:  # ignora arquivos de outro formato (ex.: saídas antigas do Gemini)
        continue
    n += 1
    ent += uso.get("prompt_tokens") or 0
    sai += uso.get("completion_tokens") or 0
    rac += (uso.get("completion_tokens_details") or {}).get("reasoning_tokens") or 0

custo = ent / 1e6 * preco_entrada + sai / 1e6 * preco_saida
print(f"{n} chamadas | entrada {ent} | saída {sai} (raciocínio {rac}) | "
      f"US$ {custo:.4f} | por chamada US$ {custo / max(n, 1):.5f}")
