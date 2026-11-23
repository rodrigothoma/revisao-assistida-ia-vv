# Oráculo — cenário C3 (não compartilhar com os revisores)

Autor: Preparador 2
Domínio (nome visível no Forms): **Frete**
Classe: `CalculadoraFrete`
Congelado em: 11/11/2026 (após piloto 2, antes da coleta definitiva). Depois disso, qualquer alteração é registrada no fim, com o motivo.

## Medidas do V_bug

- Linhas efetivas (`cloc`): 30 (V_fix: 30)
- Complexidade ciclomática somada (`lizard`): 8
- Linhas totais na imagem: 70
- Métodos: 3 (1 público, 2 privados)
- Regras numeradas no Javadoc: 4 + exceções

## Defeitos

| ID | Tipo | Método | Linhas (V_bug) | Aceitas (±2) | Regra do Javadoc violada | Categoria | Severidade | Teste gatilho | Coberto pela lista |
|---|---|---|---|---|---|---|---|---|---|
| D1 | Fronteira | `calcularFrete` | 30 | 28–32 | Regra 1 (pedidos a partir de 20000 têm frete grátis) | Incorreto | Maior | `[GATILHO D1] regra 1: valor 20000 (inclusive) têm frete grátis` | L1 |
| D2 | Regra omitida | `calcularFrete` | ausente, devia estar na 39 | 28–40 (método inteiro) | Regra 4 (frete limitado ao teto de 4500) | Ausente | Maior | `[GATILHO D2] regra 4: 8000 g fica limitado ao teto de 4500` | L2 |

**D1 — o que mudou:** `if (valorPedido >= 20000)` (V_fix) virou `if (valorPedido > 20000)` (V_bug).
- Entrada: `calcularFrete(500, 20000)`. Esperado 0, obtido 1500.

**D2 — o que mudou:** `return Math.min(total, 4500);` (V_fix) virou `return total;` (V_bug), omitindo a imposição do teto máximo de 4500 centavos.
- Entrada: `calcularFrete(8000, 5000)`. Esperado 4500, obtido 5700 (1500 + 14 × 300).

**Possíveis outros achados (OA)** previstos e que **não** são defeito:
- A divisão `pesoExcedente / 500` com incremento de 1 para o resto diferente de zero está correta para a regra "fração de 500 g".
- A validação de peso e valor do pedido fica centralizada em `validarDadosPedido`, chamada no início de `calcularFrete`.

## Sugestões entregues

| Lista | Posição | Texto de origem (arquivo/execução) | Classificação |
|---|---|---|---|
| L1 | 1 | `restrito/C3_numerado_exec1.txt`, item 1 | VP de D1 |
| L1 | 2 | `generico/C3_fix_numerado_exec1.txt`, item 1 | FP |
| L2 | 1 | `generico/C3_fix_numerado_exec1.txt`, item 1 | FP (o mesmo de L1) |
| L2 | 2 | `restrito/C3_numerado_exec1.txt`, item 2 | VP de D2 |

Textos completos em `sugestoes/listas.md`. O VP de D1 é a exec1, item 1 (linhas 30–31). O VP de D2 é a exec1, item 2 (linhas 38–39). O FP é o primeiro apontamento da exec1 do prompt genérico em V_fix (números mágicos). As linhas coincidem diretamente com o código numerado final de V_bug.

## Desempenho bruto do modelo

Modelo: openai/gpt-oss-120b (Groq), raciocínio medium, 10/11/2026. Prompt restrito em V_bug e V_fix; prompt genérico em V_fix.

| Execução | Detectou D1? | Detectou D2? | FP (V_bug) | Restrito em V_fix | Genérico em V_fix |
|---|---|---|---|---|---|
| 1 | sim | sim | 0 | 0 | 3 FP (números mágicos; overflow int inexistente; @throws) |
| 2 | sim | sim | 0 | 0 | 2 FP (números mágicos; validação de pesoExcedente) |
| 3 | sim | sim | 0 | 0 | 3 FP (números mágicos; overflow int inexistente; static) |
| 4 | sim | sim | 0 | 0 | 1 FP (@throws em validarDadosPedido) |
| 5 | sim | sim | 0 | 0 | 4 FP (declaração package; números mágicos; static; validação) |

Sensibilidade bruta (restrito, V_bug): 10/10 (100%). VPP bruto: 100%. Estabilidade: D1 5/5, D2 5/5.

**Nota sobre o suposto overflow de int:** nas execuções 1 e 3 do genérico, o modelo alegou possibilidade de overflow em `blocos * 300`. Contudo, para `pesoGramas = Integer.MAX_VALUE` (2.147.483.647), o cálculo resulta em 1.288.489.800 centavos (adicional) e 1.288.491.300 centavos (total), que não excede `Integer.MAX_VALUE`. Como o estouro é aritmeticamente impossível no código, o apontamento é uma alucinação e foi classificado como falso positivo (FP), e não como outro achado (OA).

## Alterações após o congelamento

- (nenhuma)
