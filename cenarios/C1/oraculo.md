# Oráculo — cenário C1 (não compartilhar com os revisores)

Autor: Preparador 1
Domínio (nome visível no Forms): **Estacionamento**
Classe: `CalculadoraEstacionamento`
Congelado em: 11/11/2026 (após piloto 2, antes da coleta definitiva). Depois disso, qualquer alteração é registrada no fim, com o motivo.

## Medidas do V_bug

- Linhas efetivas (`cloc`): 27 (V_fix: 31)
- Complexidade ciclomática somada (`lizard`): 7
- Linhas totais na imagem: 69
- Métodos: 3 (1 público, 2 privados)
- Regras numeradas no Javadoc: 5 + exceção

## Defeitos

| ID | Tipo | Método | Linhas (V_bug) | Aceitas (±2) | Regra do Javadoc violada | Categoria | Severidade | Teste gatilho | Coberto pela lista |
|---|---|---|---|---|---|---|---|---|---|
| D1 | Fronteira | `tarifaPorTempo` | 49 | 47–51 | Regra 1 (até 15 min, inclusive, grátis) | Incorreto | Maior | `[GATILHO D1] 15 min é grátis` | L1 |
| D2 | Regra omitida | `calcularTarifa` | ausente, devia estar após a 34 | 30–39 (método inteiro) | Regra 4 (tarifa nunca passa de 3000) | Ausente | Maior | `[GATILHO D2] 600 min limitado a 3000`, `600 min validado = 1500` | L2 |

**D1 — o que mudou:** `if (minutos <= 15)` (V_fix) virou `if (minutos < 15)` (V_bug).
- Entrada: `calcularTarifa(15, false)`. Esperado 0, obtido 800.

**D2 — o que mudou:** foi removido o bloco abaixo e a constante `TARIFA_MAXIMA = 3000`, para que nenhuma constante sem uso denuncie o defeito.

```java
if (tarifa > TARIFA_MAXIMA) {
    tarifa = TARIFA_MAXIMA;
}
```

- Entrada: `calcularTarifa(600, false)`. Esperado 3000, obtido 3500 (800 + 9 × 300).
- Com validação: esperado 1500, obtido 1750.
- O limite só é atingido acima de 480 minutos (8 horas).

**Possíveis outros achados (OA)** previstos e que **não** são defeito:
- `horasAdicionais` com `(x + 59) / 60` está correto para a regra "fração de hora".
- A divisão `tarifa / 2` arredonda para baixo, como manda a regra 5.

**Outro achado real (fora de D):** estouro de `int` em `tarifaPorTempo` para `minutos` acima de ~7,1 milhões (13 anos); com `Integer.MAX_VALUE`, V_fix devolve -2147482888. Se um revisor apontar isso, classificar como OA, não como FP.

## Sugestões entregues

| Lista | Posição | Texto de origem (arquivo/execução) | Classificação |
|---|---|---|---|
| L1 | 1 | `restrito/C1_numerado_exec1.txt`, item 1 | VP de D1 |
| L1 | 2 | `generico/C1_fix_numerado_exec4.txt`, item 1 | FP |
| L2 | 1 | `generico/C1_fix_numerado_exec4.txt`, item 1 | FP (o mesmo de L1) |
| L2 | 2 | `restrito/C1_numerado_exec1.txt`, item 2 | VP de D2 |

Textos completos em `sugestoes/listas.md`. O primeiro apontamento do prompt genérico (exec1: estouro de `int` para `minutos` enorme) foi pulado porque é **outro achado** real: `calcularTarifa(Integer.MAX_VALUE, false)` devolve -2147482888 em V_fix. As linhas do FP foram mapeadas de 70-71 (em V_fix) para 66-67 para coincidir com a imagem de V_bug vista pelo revisor.

## Desempenho bruto do modelo

Modelo: openai/gpt-oss-120b (Groq), raciocínio medium, 10/11/2026. Prompt restrito em V_bug e V_fix; prompt genérico em V_fix.

| Execução | Detectou D1? | Detectou D2? | Duplicados de D2 (V_bug) | FP (V_bug) | Restrito em V_fix | Genérico em V_fix |
|---|---|---|---|---|---|---|
| 1 | sim | sim | 1 (desconto antes do teto) | 0 | 0 | 1 OA (estouro de int) |
| 2 | sim | sim | 0 | 0 | 0 | 0 |
| 3 | sim | sim | 0 | 0 | 0 | 0 |
| 4 | sim | sim | 1 (desconto antes do teto) | 0 | 0 | 1 FP (validação de minutosExcedentes) |
| 5 | sim | sim (com a ordem do desconto no mesmo item) | 0 | 0 | 0 | 1 OA (estouro) + 2 FP (Javadoc de horasAdicionais; números mágicos) |

Sensibilidade bruta (restrito, V_bug): 10/10. VPP bruto: 100% (duplicados fora do cálculo). Estabilidade: D1 5/5, D2 5/5.

## Alterações após o congelamento

- (nenhuma)
