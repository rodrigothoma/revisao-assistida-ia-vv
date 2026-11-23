# Listas de sugestões — C2 (não compartilhar com os revisores)

Modelo: openai/gpt-oss-120b (Groq), raciocínio medium. Gerado em 10/11/2026.
Texto literal do modelo; só foram removidos a numeração, a marcação Markdown (`**` e crases) e os hífens não separáveis. As linhas do FP foram ajustadas de 72-76 (em V_fix) para 75-79 para corresponder à numeração da imagem de V_bug vista pelo revisor.

Regra de escolha (Seção 4.3 do artigo, "Listas de sugestões"): o VP é a primeira sugestão das execuções com o prompt restrito em V_bug que atende à
regra de correspondência e cujo exemplo numérico, se houver, está correto; o FP é o primeiro apontamento das execuções com o
prompt genérico em V_fix classificado como FP (apontamentos sobre documentação ou que são outro achado real são pulados).

Origem: VP de D1 = `restrito/C2_numerado_exec1.txt, item 2`; VP de D2 = `restrito/C2_numerado_exec5.txt, item 1`; FP = `generico/C2_fix_numerado_exec4.txt, item 1`.

## L1 (cobre D1; FP na posição 2)

**Sugestão 1**

Linhas: 57-62
Descrição: O método situacao verifica primeiro se a média é maior ou igual a 60 e devolve APROVADO, antes de checar a frequência. Conforme a especificação, a frequência abaixo de 75 % tem prioridade e deve resultar em REPROVADO_FREQUENCIA, independentemente da média. Assim, para frequência=70 e notas que geram média=80, o método retorna APROVADO em vez de REPROVADO_FREQUENCIA.
Categoria: incorreto
Severidade: maior

**Sugestão 2**

Linhas: 75-79
Descrição: o método validarNota não depende de estado da instância; poderia ser declarado static, evitando a necessidade de criar um objeto apenas para utilizá-lo.
Categoria: excedente (método não precisa ser de instância)
Severidade: menor.

## L2 (cobre D2; FP na posição 1)

**Sugestão 1**

Linhas: 75-79
Descrição: o método validarNota não depende de estado da instância; poderia ser declarado static, evitando a necessidade de criar um objeto apenas para utilizá-lo.
Categoria: excedente (método não precisa ser de instância)
Severidade: menor.

**Sugestão 2**

Linhas: 26-28
Descrição: O método calcularMedia altera o valor de p1 quando p2 > p1, fazendo com que a fórmula passe a usar o maior valor duas vezes (3 × p2 + 3 × p2 + 4 × trabalho). Isso gera uma média diferente da especificada, que deve ser (3 × p1 + 3 × p2 + 4 × trabalho) / 10. Exemplo: p1 = 50, p2 = 80, trabalho = 70 → esperado 67, obtido 76.
Categoria: incorreto
Severidade: maior
