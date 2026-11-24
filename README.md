# Revisão assistida por IA em V&V: pacote de replicação

## 1. O que é isto

Material do artigo **"Revisão assistida por IA em Verificação e Validação: eficiência e detecção de defeitos frente à revisão humana"**, de Artur Wahlbrink Kraemer, Fade Hassan Husein Kanaan, Gabriel Camargo Ortiz, Gustavo Fernandes dos Anjos, Matheus Domingues Cabral e Rodrigo Thoma da Silva (Squad 2, Verificação e Validação, AL0342, Universidade Federal do Pampa, 2026/2).

O estudo mediu, em um experimento com quatro revisores e quatro classes Java com defeitos semeados, o tempo de revisão e a detecção de defeitos com e sem uma lista de sugestões gerada pelo modelo gpt-oss-120b.

## 2. Como o material está organizado

```
cenarios/          os quatro cenários (C1 a C4) e o exemplo do roteiro
  C<n>/V_bug/      classe revisada, com os dois defeitos semeados
  C<n>/V_fix/      versão correta
  C<n>/testes/     testes internos, com os testes gatilho [GATILHO Dn] (não foram entregues aos revisores)
  C<n>/oraculo.md  oráculo: linhas, regra violada, categoria e teste gatilho de cada defeito
  C<n>/sugestoes/  as 15 respostas íntegras da API por cenário (.json com metadados e raciocínio; .txt com o texto)
                   e listas.md (listas L1 e L2 mostradas aos revisores)
  C<n>/C<n>.png    imagem do código com linhas numeradas, como aparecia no formulário
  prompt_sistema.txt, prompt_generico.txt   as duas instruções enviadas ao modelo, texto exato
  gerar_lote.sh, rodar_testes.sh, gerar_imagem.py
formularios/       PDFs do roteiro, do questionário de caracterização e dos 12 formulários de revisão
dados/
  sessao.md        registro da sessão de 11/11/2026 (largada, durações, interrupções)
  sorteio.md       registro do sorteio dos revisores entre R1 e R4
  coleta/          respostas anonimizadas, classificações e scripts de análise (ver bloco 6)
  piloto2/         respostas do piloto com os cenários próprios (preparadores P1 e P2)
piloto/            piloto com o Defects4J (Lang-10 e Lang-12), que motivou a troca do objeto;
                   unidades/gerar_sugestoes.py é o script de chamada à API usado também nos cenários
apendices.md       instruções ao modelo e evidência de viabilidade (antigos apêndices A e B do artigo)
```

## 3. Como reproduzir

Requisitos: Python 3.10 ou superior (testado com 3.13), sem bibliotecas externas; Java 17 (JDK) para os testes dos cenários.

```bash
# Medidas do artigo a partir dos dados (menos de 1 s)
python3 dados/coleta/analisar.py          # Tabelas 3, 4 e 5; grava revisoes.csv, triagem.csv e resumo.txt
python3 dados/coleta/kappa.py             # concordância entre preparadores nas alegações dos revisores
python3 dados/coleta/kappa.py modelo      # concordância nas 60 saídas do modelo
python3 dados/coleta/consenso.py          # Tabela 6: desempenho bruto do modelo e análise de erros

# Comprovação do oráculo (alguns segundos por cenário)
./cenarios/rodar_testes.sh C1             # V_fix passa tudo; V_bug falha só nos testes [GATILHO]
```

Gerar novas respostas do modelo exige uma chave da Groq e não reproduz o texto exato, porque a geração é estocástica (temperatura 1, sem semente fixa):

```bash
GROQ_API_KEY="..." ./cenarios/gerar_lote.sh C1   # 15 chamadas; não refaz o que já existe
python3 piloto/unidades/custo_gemini.py cenarios  # tokens e custo estimado
```

## 4. De onde vêm os dados

- **Cenários e oráculos:** escritos pelos dois preparadores em novembro de 2026; oráculos congelados em 11/11/2026, antes da coleta.
- **Respostas dos revisores:** sessão única de 11/11/2026, a distância, com quatro revisores (membros da equipe) e registro em Google Forms (`formularios/`). A planilha exportada foi reduzida a `dados/coleta/respostas_anonimizadas.csv`.
- **Anonimização:** os revisores aparecem só como R1 a R4, desde os formulários (código pré-preenchido no link); nomes e e-mails não foram coletados. O vínculo entre código e pessoa fica só com os preparadores e não é publicado. O questionário de caracterização (`caracterizacao.csv`) tem apenas respostas em faixas.
- **Classificação:** os dois preparadores classificaram de forma independente as alegações (`coleta/cego/alegacoes_P1.csv`, `alegacoes_P2.csv`) e as saídas do modelo (`modelo_P1.csv`, `modelo_P2.csv`), sem ver o revisor nem a condição (`chave.csv` desfaz o embaralhamento; `gerar_cego.py` e `gerar_modelo.py` geram essas planilhas). O consenso está em `alegacoes_consenso.csv` e `modelo_consenso.csv`; a classificação usada nas análises, em `coleta/classificacao.csv`.

## 5. O modelo usado

- **Modelo:** gpt-oss-120b (OpenAI, pesos abertos, Apache 2.0), pela API da Groq, identificador `openai/gpt-oss-120b`.
- **Execução:** 10/11/2026; a hora de cada chamada, o modelo devolvido, o `system_fingerprint`, o uso de tokens e a semente sorteada pela API estão em cada `.json`.
- **Parâmetros:** esforço de raciocínio `medium`; `max_tokens` 6.800; temperatura, top-p e demais parâmetros nos padrões da API (1 e 1).
- **Prompts:** `cenarios/prompt_sistema.txt` (restrita) e `cenarios/prompt_generico.txt` (genérica), enviados como instrução de sistema, seguidos do código numerado (`cenarios/C<n>/C<n>_numerado.txt` para V_bug, `C<n>_fix_numerado.txt` para V_fix). Cinco execuções por configuração: restrita em V_bug, restrita em V_fix e genérica em V_fix.
- O piloto com o Defects4J usou o Gemini 3.8 Flash (saídas em `piloto/unidades/saidas/`), substituído em 10/11/2026.

## 6. Mapa para o artigo

| No artigo | Arquivo que gera ou contém |
|---|---|
| Tabela 1 (quadrado latino) | `DELINEAMENTO` em `dados/coleta/analisar.py`; `dados/sorteio.md` |
| Tabela 2 (cenários) | `cenarios/C<n>/oraculo.md` (linhas `cloc`, complexidade, defeitos) |
| Tabela 3 (síntese), incluindo as leituras alternativas | `dados/coleta/analisar.py` → `resumo.txt` |
| Tabela 4 (resultados por revisão, com cobertura e triagem) | `dados/coleta/analisar.py` → `revisoes.csv` e `triagem.csv` |
| Tabela 5 (tempo por cenário) e análise sem a 1ª revisão | `dados/coleta/analisar.py` → `resumo.txt` |
| Tabela 6 (desempenho bruto do modelo) | `dados/coleta/consenso.py` → `modelo_bruto.txt`, a partir de `coleta/cego/modelo_consenso.csv` |
| Kappa e acordo (Seção 5.5) | `dados/coleta/kappa.py` e `kappa.py modelo` |
| Caracterização dos revisores (Seção 5.1) | `dados/coleta/caracterizacao.csv` |
| Durações das sessões e largada | `dados/sessao.md` e `resumo.txt` |
| Discussão (diferença por posição, detecção por metade da sessão, média por revisor) | `dados/coleta/analisar.py` → `resumo.txt` |
| Instruções ao modelo e evidência de viabilidade | `apendices.md` |

## 7. Licença e como citar

Código sob MIT ([`LICENSE`](LICENSE)); dados, cenários, respostas do modelo, formulários e documentos sob CC BY 4.0 ([`LICENSE-DADOS.md`](LICENSE-DADOS.md)).

DOI do pacote (Zenodo): *a preencher após a release v1.0*.

> KRAEMER, A. W.; KANAAN, F. H. H.; ORTIZ, G. C.; ANJOS, G. F.; CABRAL, M. D.; SILVA, R. T. Revisão assistida por IA em Verificação e Validação: eficiência e detecção de defeitos frente à revisão humana. Artigo da disciplina Verificação e Validação (AL0342), Universidade Federal do Pampa, Alegrete, 2026. Pacote de replicação: https://doi.org/10.5281/zenodo.XXXXXXX.
