# Oráculo — cenário C2 (não compartilhar com os revisores)

Autor: Preparador 1
Domínio (nome visível no Forms): **Notas da disciplina**
Classe: `AvaliacaoDisciplina`
Congelado em: 11/11/2026 (após piloto 2, antes da coleta definitiva). Depois disso, qualquer alteração é registrada no fim, com o motivo.

## Medidas do V_bug

- Linhas efetivas (`cloc`): 33 (V_fix: 30)
- Complexidade ciclomática somada (`lizard`): 11
- Linhas totais na imagem: 80
- Métodos: 3 (2 públicos, 1 privado) + enum `Situacao`
- Regras no Javadoc: fórmula da média + 4 regras de situação, em ordem de prioridade, + exceções

## Defeitos

| ID | Tipo | Método | Linhas (V_bug) | Aceitas (±2) | Regra do Javadoc violada | Categoria | Severidade | Teste gatilho | Coberto pela lista |
|---|---|---|---|---|---|---|---|---|---|
| D1 | Condição/ordem | `situacao` | 57–62 | 55–64 | Regra 1 da situação (frequência < 75% reprova "qualquer que seja a média", com prioridade) | Incorreto | Maior | `[GATILHO D1] frequência 60 com média 80` | L1 |
| D2 | Comportamento extra | `calcularMedia` | 26–28 | 24–30 | Fórmula da média (não prevê substituir a P1) | Excedente | Maior | `[GATILHO D2] P2 maior que P1 não substitui a P1` | L2 |

**D1 — o que mudou:** o bloco `if (frequencia < 75)` passou para depois de `if (media >= 60)`.
- Entrada: `situacao(80, 80, 80, 60)`. Esperado `REPROVADO_FREQUENCIA`, obtido `APROVADO`.
- Com média abaixo de 60, o resultado continua certo.

**D2 — o que mudou:** foi inserido o bloco abaixo antes do cálculo, uma "substitutiva" que o Javadoc não prevê.

```java
if (p2 > p1) {
    p1 = p2;
}
```

- Entrada: `calcularMedia(40, 80, 70)`. Esperado 64, obtido 76.

**Possíveis outros achados (OA)** previstos e que **não** são defeito:
- `situacao` chama `calcularMedia`, que valida as notas, então as exceções de nota também valem para `situacao`.
- A divisão inteira descarta a fração (58,4 vira 58), como manda o Javadoc.

## Sugestões entregues

| Lista | Posição | Texto de origem (arquivo/execução) | Classificação |
|---|---|---|---|
| L1 | 1 | `restrito/C2_numerado_exec1.txt`, item 2 | VP de D1 |
| L1 | 2 | `generico/C2_fix_numerado_exec4.txt`, item 1 | FP |
| L2 | 1 | `generico/C2_fix_numerado_exec4.txt`, item 1 | FP (o mesmo de L1) |
| L2 | 2 | `restrito/C2_numerado_exec5.txt`, item 1 | VP de D2 |

Textos completos em `sugestoes/listas.md`. Para D2, as exec1 a exec3 apontam o defeito, mas com exemplos numéricos errados (ex.: exec1 diz que 30/90/50 deveria dar 63 e dá 56; o certo é 56 e o código dá 74); foi usada a exec5, a primeira com exemplo correto (50/80/70: esperado 67, obtido 76). As linhas do FP foram mapeadas de 72-76 (em V_fix) para 75-79 para coincidir com a imagem de V_bug vista pelo revisor.

## Desempenho bruto do modelo

Modelo: openai/gpt-oss-120b (Groq), raciocínio medium, 10/11/2026. Prompt restrito em V_bug e V_fix; prompt genérico em V_fix.

| Execução | Detectou D1? | Detectou D2? | FP (V_bug) | Restrito em V_fix | Genérico em V_fix |
|---|---|---|---|---|---|
| 1 | sim | sim (exemplo numérico errado) | 0 | 0 | 0 |
| 2 | sim | sim (exemplo numérico errado) | 0 | 0 | 0 |
| 3 | sim | sim (exemplo numérico errado) | 0 | 0 | 0 |
| 4 | sim | **não** (apontou e, no próprio texto, concluiu que não era defeito) | 0 | 0 | 1 FP (validarNota poderia ser static) |
| 5 | sim | sim | 0 | 0 | 1 FP (cálculo da média antes da frequência, desempenho) |

Sensibilidade bruta (restrito, V_bug): 9/10. VPP bruto: 100%. Estabilidade: D1 5/5, D2 4/5.

## Alterações após o congelamento

- (nenhuma)
