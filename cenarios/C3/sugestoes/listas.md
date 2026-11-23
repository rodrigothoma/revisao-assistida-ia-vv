# Listas de sugestões — C3 (não compartilhar com os revisores)

Modelo: openai/gpt-oss-120b (Groq), raciocínio medium. Gerado em 10/11/2026.
Texto literal do modelo; só foram removidos a numeração, a marcação Markdown (`**` e crases) e os hífens não separáveis.

Regra de escolha (Seção 4.3 do artigo, "Listas de sugestões"): o VP é a primeira sugestão das execuções com o prompt restrito em V_bug que atende à regra de correspondência e cujo exemplo numérico, se houver, está correto; o FP é o primeiro apontamento das execuções com o prompt genérico em V_fix classificado como FP (apontamentos sobre documentação ou que são outro achado real são pulados).

Origem: VP de D1 = `restrito/C3_numerado_exec1.txt, item 1`; VP de D2 = `restrito/C3_numerado_exec1.txt, item 2`; FP = `generico/C3_fix_numerado_exec1.txt, item 1`.

## L1 (cobre D1; FP na posição 2)

**Sugestão 1**

Linhas: 30-31
Descrição: O método retorna tarifa zero somente quando {@code valorPedido} é maior que 20000 centavos. Conforme o Javadoc, pedidos com valor a partir de 20000 centavos, inclusive, devem ter tarifa zero. Assim, para {@code valorPedido} = 20000 o método devolve 1500 (ou outro cálculo) ao invés de 0.
Categoria: incorreto
Severidade: maior

**Sugestão 2**

Linhas: 30, 33, 34, 36, 38, 39, 64, 66, 68
Descrição: O código utiliza valores literais (1500, 20000, 1000, 500, 300, 4500) espalhados pelo método. Esses “números mágicos” dificultam a manutenção e a compreensão, pois não há contexto explicativo nem possibilidade de alteração centralizada.
Categoria: excedente
Severidade: menor

## L2 (cobre D2; FP na posição 1)

**Sugestão 1**

Linhas: 30, 33, 34, 36, 38, 39, 64, 66, 68
Descrição: O código utiliza valores literais (1500, 20000, 1000, 500, 300, 4500) espalhados pelo método. Esses “números mágicos” dificultam a manutenção e a compreensão, pois não há contexto explicativo nem possibilidade de alteração centralizada.
Categoria: excedente
Severidade: menor

**Sugestão 2**

Linhas: 38-39 (e ausência de verificação posterior)
Descrição: O Javadoc especifica que “o valor final cobrado não pode exceder o teto de 4500 centavos”. O código calcula o total (base + adicional) e o devolve sem aplicar esse limite, podendo retornar valores superiores a 4500 centavos.
Categoria: ausente
Severidade: maior
