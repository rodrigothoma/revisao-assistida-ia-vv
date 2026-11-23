"""Concordância entre os dois preparadores (percentual de acordo e kappa de Cohen).

Lê cego/alegacoes_P1.csv e cego/alegacoes_P2.csv já preenchidos. O rótulo
comparado é a classe junto com o defeito (VP-D1, VP-D2, FP, OA, DUP).
Mostra o resultado no total e por cenário e lista as divergências, que
depois são discutidas até o consenso.

Limiar (Baltes et al., 2026): < 0,667 refazer; 0,667-0,8 provisório; > 0,8 confiável.

Uso: python3 dados/coleta/kappa.py           (alegações dos revisores)
     python3 dados/coleta/kappa.py modelo    (saídas do modelo; linhas com item 0 são ignoradas)
"""
import csv
import sys
from collections import Counter
from pathlib import Path

PASTA = Path(__file__).resolve().parent / "cego"


def rotulo(d):
    classe = d["classe"].strip().upper()
    return f"{classe}-{d['defeito'].strip().upper()}" if classe == "VP" else classe


def kappa(a, b):
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(a) | set(b)) / n ** 2
    k = None if pe == 1 else (po - pe) / (1 - pe)
    return po, k


def faixa(k):
    if k is None:
        return "indefinido (os dois usaram um único rótulo)"
    return "refazer" if k < 0.667 else "provisório" if k <= 0.8 else "confiável"


def ler(prefixo):
    """Devolve {código: (cenário, rótulo)} de um arquivo preenchido."""
    out = {}
    for d in csv.DictReader(open(PASTA / f"{prefixo}.csv", encoding="utf-8")):
        if "codigo" in d:
            out[d["codigo"]] = (d["cenario"], rotulo(d) if d["classe"].strip() else "")
        elif d["item"] != "0":
            cod = f'{d["cenario"]}/{d["instrucao"]}/{d["versao"]}/exec{d["execucao"]}/item{d["item"]}'
            out[cod] = (d["cenario"], d["rotulo"].strip().upper())
    return out


def main():
    nome = "modelo" if sys.argv[1:] == ["modelo"] else "alegacoes"
    a, b = ler(f"{nome}_P1"), ler(f"{nome}_P2")
    vazios = sorted(c for c in a if not a[c][1] or not b[c][1])
    if vazios:
        raise SystemExit(f"Classificação incompleta ({len(vazios)}): {vazios[:10]}")
    pares = [(a[c][0], a[c][1], b[c][1], c) for c in a]
    grupos = [("Total", pares)] + [(c, [p for p in pares if p[0] == c]) for c in sorted({p[0] for p in pares})]
    for nome, g in grupos:
        po, k = kappa([p[1] for p in g], [p[2] for p in g])
        ks = "--" if k is None else f"{k:.3f}"
        print(f"{nome:6} n={len(g):2}  acordo={100 * po:5.1f}%  kappa={ks}  {faixa(k)}")
    div = [p for p in pares if p[1] != p[2]]
    print(f"\nDivergências ({len(div)}):")
    for c, a, b, cod in div:
        print(f"  {cod} ({c}): P1={a}  P2={b}")


if __name__ == "__main__":
    main()
