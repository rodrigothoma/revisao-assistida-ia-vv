"""Gera as planilhas para a classificação independente das 60 saídas do modelo.

Saídas em dados/coleta/cego/: modelo_P1.csv e modelo_P2.csv, uma linha por
apontamento de cada saída (cenarios/C*/sugestoes/{restrito,generico}/*.txt).
Saídas sem apontamento viram uma linha com item 0, só para conferência.

Colunas a preencher por cada preparador:
  rotulo        VP-D1, VP-D2, FP, OA ou DUP (restrita em V_bug); FP ou OA (genérica)
  exemplo_errado  "sim" se o exemplo numérico do apontamento estiver errado
  retirado      "sim" se o próprio modelo concluiu, no texto, que não é defeito
  justificativa uma frase

Uso: python3 dados/coleta/gerar_modelo.py
"""
import csv
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
SAIDA = Path(__file__).resolve().parent / "cego"
ITEM = re.compile(r"^\s*(\d+)\.\s*\**\s*Linhas?\**\s*:\s*(.*)$", re.I)


def itens(texto):
    """Divide a resposta em apontamentos numerados ("1. Linhas: ...")."""
    blocos, atual = [], None
    for linha in texto.splitlines():
        m = ITEM.match(linha)
        if m:
            atual = {"item": int(m.group(1)), "linhas": m.group(2).strip(), "texto": []}
            blocos.append(atual)
        elif atual is not None:
            atual["texto"].append(linha.strip())
    for b in blocos:
        b["texto"] = " ".join(t for t in b["texto"] if t)
    return blocos


def main():
    linhas = []
    for cen in ("C1", "C2", "C3", "C4"):
        for instr in ("restrito", "generico"):
            for arq in sorted((RAIZ / "cenarios" / cen / "sugestoes" / instr).glob("*.txt")):
                versao = "V_fix" if "_fix_" in arq.name else "V_bug"
                execu = re.search(r"exec(\d+)", arq.name).group(1)
                base = {"cenario": cen, "instrucao": "restrita" if instr == "restrito" else "generica",
                        "versao": versao, "execucao": execu, "arquivo": arq.relative_to(RAIZ).as_posix()}
                its = itens(arq.read_text(encoding="utf-8"))
                if not its:
                    its = [{"item": 0, "linhas": "", "texto": arq.read_text(encoding="utf-8").strip()[:200]}]
                for it in its:
                    linhas.append({**base, **it, "rotulo": "", "exemplo_errado": "", "retirado": "", "justificativa": ""})
    SAIDA.mkdir(exist_ok=True)
    for prep in ("P1", "P2"):
        with open(SAIDA / f"modelo_{prep}.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(linhas[0].keys()))
            w.writeheader()
            w.writerows(linhas)
    resumo = {}
    for l in linhas:
        k = (l["cenario"], l["instrucao"], l["versao"])
        resumo[k] = resumo.get(k, 0) + (l["item"] > 0)
    for k, n in sorted(resumo.items()):
        print(*k, f"{n} apontamentos")
    print(f"total: {len(linhas)} linhas em {SAIDA}")


if __name__ == "__main__":
    main()
