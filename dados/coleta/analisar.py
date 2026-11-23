"""Análise da coleta de 11/11/2026 (R1 a R4).

Lê as respostas anonimizadas dos formulários (respostas_anonimizadas.csv) e a
classificação por alegação (classificacao.csv) e gera, nesta pasta:

  revisoes.csv   uma linha por revisão: tempo, D1, D2, VP, FP, EDE, VPP
  triagem.csv    decisão sobre cada sugestão das listas
  resumo.txt     medidas agregadas usadas no artigo

Uso: python3 dados/coleta/analisar.py   (só Python 3, sem dependências)

respostas_anonimizadas.csv foi extraída da planilha exportada do Google Forms,
com só R1 a R4 (sem o piloto) e sem os links dos formulários; o horário de
envio tem precisão de milissegundos, como na planilha.

Regras aplicadas (decididas pela equipe, 15/11/2026):
  - o relatório final é a página de apontamentos; um relatório vazio tem
    EDE 0 e VPP indefinido (análise principal), e há duas leituras de
    sensibilidade: excluir a revisão e contar a triagem como relatório;
  - um apontamento com várias alegações é dividido por alegação;
  - aceitar uma sugestão na triagem não conta como detecção.
"""
import csv
import datetime as dt
from pathlib import Path

AQUI = Path(__file__).resolve().parent
DIA = dt.date(2026, 11, 11)
LARGADA = dt.datetime(2026, 11, 11, 14, 50, 0)  # anotada pelo supervisor
REVISORES = ["R1", "R2", "R3", "R4"]
# Quadrado latino (Tabela 1 do artigo): ordem dos formulários de cada revisor.
DELINEAMENTO = {
    "R1": ["C1-H", "C2-L1", "C3-H", "C4-L2"],
    "R2": ["C2-H", "C1-L2", "C4-H", "C3-L1"],
    "R3": ["C3-L2", "C4-H", "C1-L1", "C2-H"],
    "R4": ["C4-L1", "C3-H", "C2-L2", "C1-H"],
}
# Lista -> defeito coberto; posição do FP na lista.
COBERTO = {"L1": "D1", "L2": "D2"}
POS_FP = {"L1": 2, "L2": 1}


def ler_respostas():
    """Devolve {(revisor, formulário): {campo: valor, "envio": datetime}}."""
    respostas = {}
    with open(AQUI / "respostas_anonimizadas.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            d = respostas.setdefault((r["revisor"], r["formulario"]), {})
            hora = dt.datetime.strptime(r["envio"], "%H:%M:%S.%f").time()
            d["envio"] = dt.datetime.combine(DIA, hora)
            d[r["campo"]] = r["valor"]
    # Confere que os envios seguiram a ordem do delineamento.
    for rv, forms in DELINEAMENTO.items():
        envios = [respostas[(rv, f)]["envio"] for f in forms]
        assert envios == sorted(envios), f"{rv} não seguiu a ordem da Tabela 1"
    return respostas


def main():
    respostas = ler_respostas()
    classif = list(csv.DictReader(open(AQUI / "classificacao.csv", encoding="utf-8")))

    revisoes, triagem = [], []
    for rv in REVISORES:
        anterior = LARGADA
        for ordem, form in enumerate(DELINEAMENTO[rv], 1):
            cen, versao = form.split("-")
            env = respostas[(rv, form)]["envio"]
            seg = (env - anterior).total_seconds()
            anterior = env
            al = [c for c in classif if c["revisor"] == rv and c["formulario"] == form]
            vp = [c for c in al if c["classe"] == "VP"]
            fp = [c for c in al if c["classe"] == "FP"]
            achou = {c["defeito"] for c in vp}
            reg = {
                "revisor": rv, "ordem": ordem, "cenario": cen,
                "condicao": "H" if versao == "H" else "A",
                "lista": "" if versao == "H" else versao,
                "tempo_s": round(seg), "D1": int("D1" in achou), "D2": int("D2" in achou),
                "VP": len(vp), "FP": len(fp),
            }
            reg["EDE"] = 50 * (reg["D1"] + reg["D2"])
            reg["VPP"] = "" if not (vp or fp) else round(100 * len(vp) / (len(vp) + len(fp)))
            revisoes.append(reg)
            if versao != "H":
                d = respostas[(rv, form)]
                for pos in (1, 2):
                    tipo = "FP" if pos == POS_FP[versao] else "VP"
                    dec = d[f"Decisão sobre a sugestão {pos}"]
                    triagem.append({
                        "revisor": rv, "ordem": ordem, "cenario": cen, "lista": versao,
                        "posicao": pos, "sugestao": tipo + ("" if tipo == "FP" else " " + COBERTO[versao]),
                        "decisao": "aceita" if dec.startswith("Aceito") else "descartada",
                        "no_relatorio": int(tipo == "VP" and COBERTO[versao] in achou),
                    })

    for nome, linhas in (("revisoes.csv", revisoes), ("triagem.csv", triagem)):
        with open(AQUI / nome, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(linhas[0].keys()))
            w.writeheader()
            w.writerows(linhas)

    # Medidas agregadas.
    out = []
    mmss = lambda s: f"{int(s) // 60}:{int(round(s)) % 60:02d}"
    H = [r for r in revisoes if r["condicao"] == "H"]
    A = [r for r in revisoes if r["condicao"] == "A"]
    th = sum(r["tempo_s"] for r in H) / len(H)
    ta = sum(r["tempo_s"] for r in A) / len(A)
    med = lambda xs: (sorted(xs)[len(xs) // 2 - 1] + sorted(xs)[len(xs) // 2]) / 2
    out.append(f"T_H = {th:.0f} s ({mmss(th)}); T_A = {ta:.0f} s ({mmss(ta)}); E_liq = {100 * (th - ta) / th:.1f}%")
    out.append(f"medianas: H {mmss(med([r['tempo_s'] for r in H]))}; A {mmss(med([r['tempo_s'] for r in A]))}")
    out.append(f"revisões > 15 min: H {sum(r['tempo_s'] > 900 for r in H)}; A {sum(r['tempo_s'] > 900 for r in A)}")
    for c in ("C1", "C2", "C3", "C4"):
        h = sum(r["tempo_s"] for r in H if r["cenario"] == c) / 2
        a = sum(r["tempo_s"] for r in A if r["cenario"] == c) / 2
        out.append(f"  {c}: T_H {mmss(h)}  T_A {mmss(a)}  E_liq {100 * (h - a) / h:.1f}%")
    for rv in REVISORES:
        total = sum(r["tempo_s"] for r in revisoes if r["revisor"] == rv)
        out.append(f"  {rv}: sessão de {mmss(total)}")

    def ede(regs, quais=("D1", "D2")):
        n = sum(r[d] for r in regs for d in quais)
        return n, len(regs) * len(quais)

    cob = [(r, COBERTO[r["lista"]]) for r in A]
    nc = [(r, "D2" if d == "D1" else "D1") for r, d in cob]
    def taxa(pares, excluir=None):
        p = [(r, d) for r, d in pares if (r["revisor"], r["cenario"]) != excluir]
        return sum(r[d] for r, d in p), len(p)
    n, t = ede(H); out.append(f"EDE H = {n}/{t}")
    n, t = ede(A); out.append(f"EDE A = {n}/{t}")
    out.append(f"EDE A coberto = {taxa(cob)[0]}/{taxa(cob)[1]}; não coberto = {taxa(nc)[0]}/{taxa(nc)[1]}")
    ex = ("R3", "C1")
    out.append(f"  sem R3/C1: A {sum(r['D1'] + r['D2'] for r in A if (r['revisor'], r['cenario']) != ex)}/14;"
               f" coberto {taxa(cob, ex)[0]}/{taxa(cob, ex)[1]}; não coberto {taxa(nc, ex)[0]}/{taxa(nc, ex)[1]}")
    # Segunda leitura alternativa: conta como detecção o VP aceito na triagem
    # e ausente do relatório (dispensa a regra 3).
    creditar = {(t["revisor"], t["cenario"]) for t in triagem
                if t["sugestao"] != "FP" and t["decisao"] == "aceita" and not t["no_relatorio"]}
    cob_alt = sum(r[d] or (r["revisor"], r["cenario"]) in creditar for r, d in cob)
    out.append(f"  creditando VP aceitos e não relatados {sorted(creditar)}: A {ede(A)[0] + len(creditar)}/16;"
               f" coberto {cob_alt}/8; não coberto {taxa(nc)[0]}/8")
    # Tempo sem a primeira revisão de cada revisor (largada anotada ao minuto).
    h2 = [r["tempo_s"] for r in H if r["ordem"] > 1]
    a2 = [r["tempo_s"] for r in A if r["ordem"] > 1]
    th2, ta2 = sum(h2) / len(h2), sum(a2) / len(a2)
    out.append(f"sem a 1ª revisão: T_H {mmss(th2)}; T_A {mmss(ta2)}; E_liq {100 * (th2 - ta2) / th2:.1f}%")
    out.append(f"EDE H por tipo: d1 {ede(H, ('D1',))[0]}/8; d2 {ede(H, ('D2',))[0]}/8")
    for cond, regs in (("H", H), ("A", A)):
        vp = sum(r["VP"] for r in regs); fp = sum(r["FP"] for r in regs)
        out.append(f"VPP {cond} = {vp}/{vp + fp} ({100 * vp / (vp + fp):.0f}%)")
    fps = [t for t in triagem if t["sugestao"] == "FP"]
    vps = [t for t in triagem if t["sugestao"] != "FP"]
    out.append(f"FP aceitos na triagem: {sum(t['decisao'] == 'aceita' for t in fps)}/{len(fps)}"
               f" (posição 1: {sum(t['decisao'] == 'aceita' for t in fps if t['posicao'] == 1)}/4;"
               f" posição 2: {sum(t['decisao'] == 'aceita' for t in fps if t['posicao'] == 2)}/4)")
    out.append(f"VP descartados na triagem: {sum(t['decisao'] == 'descartada' for t in vps)}/{len(vps)};"
               f" VP aceitos e ausentes do relatório: {sum(t['decisao'] == 'aceita' and not t['no_relatorio'] for t in vps)}")
    texto = "\n".join(out)
    (AQUI / "resumo.txt").write_text(texto + "\n", encoding="utf-8")
    print(texto)


if __name__ == "__main__":
    main()
