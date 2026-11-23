"""Gera a planilha cega para a classificação independente dos preparadores.

Saídas em dados/coleta/cego/:
  alegacoes_P1.csv, alegacoes_P2.csv  uma cópia para cada preparador preencher
  chave.csv                           código -> revisor, formulário, apontamento
                                      (NÃO abrir antes de terminar a classificação)

As alegações vêm de classificacao.csv (só as colunas de identificação e as
linhas; a classe e o defeito não são copiados) e o texto vem de
respostas_anonimizadas.csv. Revisor, condição, lista, categoria, severidade e origem
são omitidos, e a ordem é embaralhada com semente fixa.

Uso: python3 dados/coleta/gerar_cego.py [pasta_de_saida]
Sem argumento, grava em cego/, mas recusa sobrescrever planilhas já
preenchidas; para conferir a geração, passe outra pasta.
"""
import csv
import random
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
SEMENTE = 20261115

# Texto de cada alegação nos apontamentos divididos (decisão de 15/11/2026).
DIVISOES = {
    ("R3", "C3-L2", "1", "1"): 'linha 30 contém erro de comparador, no texto diz 20.000 inclusive ou seja, deveria ser ">=" e não ">"',
    ("R3", "C3-L2", "1", "2"): "na linha 36 o valor da subtração será negativo, que vai influenciar ao somar com a variável total na linha 38",
    ("R3", "C3-L2", "1", "3"): "na linha 63, está ocorrendo o resto da divisão, caso o valor superior a 1000 não seja divisível por 500 mesmo que ultrapasse 1000, não será feito a operação corretamente",
    ("R3", "C2-H", "1", "1"): "a comparação da linha 26,e atribuir uma nota menor a prova que obteve maior nota não faz sentido",
    ("R3", "C2-H", "1", "2"): "os condicionais de comparação de presença estão incompletos, na linha 57 compara-se somente a média e não considera-se a frequência, na linha 63 compara somente a média sem levar em consideração a frequencia",
}


def main():
    texto = {}
    with open(AQUI / "respostas_anonimizadas.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            campo = r["campo"]
            if campo.startswith("Apontamento ") and campo.endswith(" - Descrição"):
                n = campo.split()[1]
                texto[(r["revisor"], r["formulario"], n)] = " ".join(r["valor"].split())

    itens = []
    for c in csv.DictReader(open(AQUI / "classificacao.csv", encoding="utf-8")):
        k = (c["revisor"], c["formulario"], c["apontamento"], c["alegacao"])
        t = DIVISOES.get(k, texto[k[:3]])
        itens.append({"chave": k, "cenario": c["formulario"].split("-")[0], "linhas": c["linhas"], "texto": t})

    random.Random(SEMENTE).shuffle(itens)
    pasta = Path(sys.argv[1]) if len(sys.argv) > 1 else AQUI / "cego"
    pasta.mkdir(parents=True, exist_ok=True)
    for prep in ("P1", "P2"):
        arq = pasta / f"alegacoes_{prep}.csv"
        if arq.exists() and any(d["classe"].strip() for d in csv.DictReader(open(arq, encoding="utf-8"))):
            raise SystemExit(f"{arq} já tem classificações; passe outra pasta de saída.")
    campos = ["codigo", "cenario", "linhas", "texto", "classe", "defeito", "justificativa"]
    for prep in ("P1", "P2"):
        with open(pasta / f"alegacoes_{prep}.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=campos)
            w.writeheader()
            for i, it in enumerate(itens, 1):
                w.writerow({"codigo": f"A{i:02d}", "cenario": it["cenario"], "linhas": it["linhas"],
                            "texto": it["texto"], "classe": "", "defeito": "", "justificativa": ""})
    with open(pasta / "chave.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["codigo", "revisor", "formulario", "apontamento", "alegacao"])
        for i, it in enumerate(itens, 1):
            w.writerow([f"A{i:02d}", *it["chave"]])
    print(f"{len(itens)} alegações em {pasta}")


if __name__ == "__main__":
    main()
