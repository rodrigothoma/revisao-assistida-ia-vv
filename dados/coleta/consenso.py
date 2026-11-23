"""Consenso entre P1 e P2 e medidas brutas do modelo.

Gera em dados/coleta/:
  cego/alegacoes_consenso.csv   classificação final das alegações dos revisores
  cego/modelo_consenso.csv      classificação final das saídas do modelo
  modelo_bruto.txt              sensibilidade, VPP, estabilidade e análise de erro do modelo

As decisões de consenso estão em CONSENSO_* abaixo, cada uma com o motivo.
Uso: python3 dados/coleta/consenso.py
"""
import csv
from collections import Counter, defaultdict
from pathlib import Path

AQUI = Path(__file__).resolve().parent
CEGO = AQUI / "cego"

# Alegações: P1 e P2 concordaram em todas; A18 foi marcada "VP/FP" pelo P1 e resolvida como VP-D1
# (a alegação aponta a linha 57 e descreve a ordem média/frequência, que é D1; a parte sobre a linha 63
# está errada, mas não muda a correspondência pela regra da Seção 4.5).
CONSENSO_ALEGACOES = {"A18": ("VP", "D1")}

# Modelo: (arquivo, item) -> campos finais.
CONSENSO_MODELO = {
    # Estouro de int real: calcularTarifa(Integer.MAX_VALUE, false) devolve -2147482888 em V_fix (OA no oráculo de C1).
    ("cenarios/C1/sugestoes/generico/C1_fix_numerado_exec1.txt", "1"): {"rotulo": "OA"},
    ("cenarios/C1/sugestoes/generico/C1_fix_numerado_exec5.txt", "1"): {"rotulo": "OA"},
    # Estouro alegado em C3 não ocorre: calcularFrete(Integer.MAX_VALUE, 1) devolve 4500 em V_fix -> FP (P2).
    # Exemplos numéricos conferidos e errados (P1):
    ("cenarios/C3/sugestoes/restrito/C3_numerado_exec3.txt", "2"): {"exemplo_errado": "sim"},  # 3000 g dá 2700, não 2100
    ("cenarios/C4/sugestoes/restrito/C4_numerado_exec2.txt", "1"): {"exemplo_errado": "sim"},  # 5 dias: código dá 2350, não 2050
    ("cenarios/C4/sugestoes/restrito/C4_numerado_exec4.txt", "1"): {"exemplo_errado": "sim"},  # 4 dias: código dá 2000, não 1300
    ("cenarios/C4/sugestoes/restrito/C4_numerado_exec5.txt", "1"): {"exemplo_errado": "sim"},  # 5 dias: 2350 e 1300, não 2150 e 1500
}


def ler(nome):
    with open(CEGO / nome, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def gravar(nome, linhas):
    with open(CEGO / nome, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0].keys()))
        w.writeheader()
        w.writerows(linhas)


def sim(v):
    return v.strip().lower() == "sim"


def main():
    al = ler("alegacoes_P2.csv")
    for a in al:
        if a["codigo"] in CONSENSO_ALEGACOES:
            a["classe"], a["defeito"] = CONSENSO_ALEGACOES[a["codigo"]]
    gravar("alegacoes_consenso.csv", al)

    mo = ler("modelo_P2.csv")
    for m in mo:
        for k, v in CONSENSO_MODELO.get((m["arquivo"], m["item"]), {}).items():
            m[k] = v
    gravar("modelo_consenso.csv", mo)

    out = []
    total_det = total_op = 0
    erros = Counter()
    for cen in ("C1", "C2", "C3", "C4"):
        rb = [m for m in mo if m["cenario"] == cen and m["instrucao"] == "restrita" and m["versao"] == "V_bug"]
        execs = sorted({m["execucao"] for m in rb})
        det = defaultdict(set)
        vp = fp = dup = oa = 0
        for m in rb:
            if m["item"] == "0":
                continue
            r = m["rotulo"].strip().upper()
            if sim(m["retirado"]):
                erros["apontamento retirado pelo próprio modelo"] += 1
                continue
            if r.startswith("VP-"):
                det[r[3:]].add(m["execucao"])
                vp += 1
            elif r == "DUP":
                dup += 1
            elif r == "FP":
                fp += 1
            elif r == "OA":
                oa += 1
            if sim(m["exemplo_errado"]):
                erros["exemplo numérico incorreto"] += 1
        erros["apontamento duplicado"] += dup
        for d in ("D1", "D2"):
            n = len(det[d])
            total_det += n
            total_op += len(execs)
            if n < len(execs):
                erros["defeito não apontado"] += len(execs) - n
        vpp = "indef." if vp + fp == 0 else f"{100 * vp / (vp + fp):.0f}%"
        rf = [m for m in mo if m["cenario"] == cen and m["instrucao"] == "restrita" and m["versao"] == "V_fix" and m["item"] != "0"]
        gf = [m for m in mo if m["cenario"] == cen and m["instrucao"] == "generica" and m["item"] != "0"]
        gfp = sum(m["rotulo"].strip().upper() == "FP" for m in gf)
        goa = sum(m["rotulo"].strip().upper() == "OA" for m in gf)
        erros["apontamento fora do Javadoc (instrução genérica)"] += gfp
        out.append(f"{cen}: D1 {len(det['D1'])}/{len(execs)}, D2 {len(det['D2'])}/{len(execs)} | "
                   f"restrita V_bug: VP {vp}, DUP {dup}, FP {fp}, OA {oa}, VPP {vpp} | "
                   f"restrita V_fix: {len(rf)} apontamentos | genérica V_fix: {gfp} FP, {goa} OA")
    out.insert(0, f"Sensibilidade bruta (restrita, V_bug, sem retirados): {total_det}/{total_op}")
    out.append("Análise de erro do modelo (restrita em V_bug, salvo indicação):")
    out += [f"  {k}: {v}" for k, v in erros.most_common()]
    (AQUI / "modelo_bruto.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
    print("\n".join(out))


if __name__ == "__main__":
    main()
