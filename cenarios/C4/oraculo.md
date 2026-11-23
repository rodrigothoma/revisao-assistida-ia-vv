# Oráculo — cenário C4 (não compartilhar com os revisores)

Autor: Preparador 2
Domínio (nome visível no Forms): **Biblioteca**
Classe: `CalculadoraMulta`
Congelado em: 11/11/2026 (após piloto 2, antes da coleta definitiva). Depois disso, qualquer alteração é registrada no fim, com o motivo.

## Medidas do V_bug

- Linhas efetivas (`cloc`): 27 (V_fix: 27)
- Complexidade ciclomática somada (`lizard`): 8
- Linhas totais na imagem: 74
- Métodos: 4 (1 público, 3 privados)
- Regras numeradas no Javadoc: 4 + exceções

## Defeitos

| ID | Tipo | Método | Linhas (V_bug) | Aceitas (±2) | Regra do Javadoc violada | Categoria | Severidade | Teste gatilho | Coberto pela lista |
|---|---|---|---|---|---|---|---|---|---|
| D1 | Expressão / fórmula | `calcularValorBase` | 58 | 56–60 | Regra 2 (350 por dia adicional a partir do 4º dia) | Incorreto | Maior | `[GATILHO D1] regra 2: 5 dias de atraso` | L1 |
| D2 | Comportamento extra | `aplicarRegraReserva` | 70 | 68–72 | Regra 3 (reserva técnica apenas dobra a multa) | Excedente | Maior | `[GATILHO D2] regra 3: 2 dias reserva tecnica` | L2 |

**D1 — o que mudou:** `return (3 * 200) + ((diasAtraso - 3) * 350);` (V_fix) virou `return (3 * 200) + (diasAtraso * 350);` (V_bug), aplicando a taxa de 350 a todos os dias em vez de apenas aos excedentes.
- Entrada: `calcularMulta(5, false)`. Esperado 1300, obtido 2350.

**D2 — o que mudou:** `return valorBase * 2;` (V_fix) virou `return (valorBase * 2) + 500;` (V_bug), inserindo uma taxa administrativa de 500 centavos que o Javadoc não prevê.
- Entrada: `calcularMulta(2, true)`. Esperado 800, obtido 1300.

**Possíveis outros achados (OA)** previstos e que **não** são defeito:
- A validação de dias de atraso fica centralizada em `validarDiasAtraso`, chamada no início de `calcularMulta`.
- A regra de reserva técnica multiplica o valor já consolidado após o cálculo base.

**Nota sobre a cobertura de testes:** como qualquer caso de teste que exercite a Regra 2 (`diasAtraso >= 4`) ou a Regra 3 (`ehExemplarReserva = true`) atinge os métodos modificados em V_bug, os testes dessas duas regras são necessariamente os testes gatilho de D1 e D2 (falham em V_bug e passam em V_fix). Os demais testes da suíte (Regra 1 e exceções) passam em ambas as versões.

## Sugestões entregues

| Lista | Posição | Texto de origem (arquivo/execução) | Classificação |
|---|---|---|---|
| L1 | 1 | `restrito/C4_numerado_exec1.txt`, item 1 | VP de D1 |
| L1 | 2 | `generico/C4_fix_numerado_exec1.txt`, item 2 | FP |
| L2 | 1 | `generico/C4_fix_numerado_exec1.txt`, item 2 | FP (o mesmo de L1) |
| L2 | 2 | `restrito/C4_numerado_exec1.txt`, item 2 | VP de D2 |

Textos completos em `sugestoes/listas.md`. O VP de D1 é a exec1, item 1 (linha 58, cálculo exato para 5 dias: 1300 esperado vs 2350 obtido). O VP de D2 é a exec1, item 2 (linha 70, cálculo exato para valorBase = 1000 com reserva: 2000 esperado vs 2500 obtido). O FP é a exec1, item 2 do prompt genérico em V_fix (linhas 54–59, números mágicos em calcularValorBase), pulando o item 1 (falta de @throws em Javadoc de método privado) por se tratar de apontamento sobre documentação e não sobre o código. As linhas coincidem diretamente com o código numerado final de V_bug.

## Desempenho bruto do modelo

Modelo: openai/gpt-oss-120b (Groq), raciocínio medium, 10/11/2026. Prompt restrito em V_bug e V_fix; prompt genérico em V_fix.

| Execução | Detectou D1? | Detectou D2? | FP (V_bug) | Restrito em V_fix | Genérico em V_fix |
|---|---|---|---|---|---|
| 1 | sim | sim | 0 | 0 | 4 FP (@throws; números mágicos; static; package) |
| 2 | sim | sim | 0 | 0 | 0 |
| 3 | sim | sim | 0 | 0 | 0 |
| 4 | sim | sim | 0 | 0 | 5 FP (números mágicos; static; package; tipo int; overflow reserva inexistente) |
| 5 | sim | sim | 0 | 0 | 0 |

Sensibilidade bruta (restrito, V_bug): 10/10 (100%). VPP bruto: 100%. Estabilidade: D1 5/5, D2 5/5.

**Nota sobre o suposto overflow em aplicarRegraReserva:** na execução 4 (item 5) do genérico, o modelo apontou risco de overflow silencioso ao multiplicar `valorBase * 2`. Contudo, `validarDiasAtraso` limita os dias de atraso a no máximo 120, gerando multa máxima de 83.100 centavos com reserva técnica, muito distante de `Integer.MAX_VALUE` (2.147.483.647). Como o estouro é impossível, o apontamento é uma alucinação e foi classificado como falso positivo (FP), e não como outro achado (OA).

## Alterações após o congelamento

- (nenhuma)
