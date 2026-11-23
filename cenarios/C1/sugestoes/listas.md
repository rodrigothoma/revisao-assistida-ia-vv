# Listas de sugestões — C1 (não compartilhar com os revisores)

Modelo: openai/gpt-oss-120b (Groq), raciocínio medium. Gerado em 10/11/2026.
Texto literal do modelo; só foram removidos a numeração, a marcação Markdown (`**` e crases) e os hífens não separáveis. As linhas do FP foram ajustadas de 70-71 (em V_fix) para 66-67 para corresponder à numeração da imagem de V_bug vista pelo revisor.

Regra de escolha (Seção 4.3 do artigo, "Listas de sugestões"): o VP é a primeira sugestão das execuções com o prompt restrito em V_bug que atende à
regra de correspondência e cujo exemplo numérico, se houver, está correto; o FP é o primeiro apontamento das execuções com o
prompt genérico em V_fix classificado como FP (apontamentos sobre documentação ou que são outro achado real são pulados).

Origem: VP de D1 = `restrito/C1_numerado_exec1.txt, item 1`; VP de D2 = `restrito/C1_numerado_exec1.txt, item 2`; FP = `generico/C1_fix_numerado_exec4.txt, item 1`.

## L1 (cobre D1; FP na posição 2)

**Sugestão 1**

Linhas: 49-50
Descrição: A tarifa deve ser gratuita para permanências de até 15 minutos, inclusive. O código usa if (minutos < 15), de modo que para minutos == 15 a tarifa retornada é 800 em vez de 0.
Categoria: incorreto
Severidade: maior

**Sugestão 2**

Linhas: 66-67
Descrição: O Javadoc de horasAdicionais especifica que o parâmetro minutosExcedentes deve ser maior que zero, porém o método aceita zero (ou valores negativos) e simplesmente calcula (minutosExcedentes + 59) / 60, retornando 0 para zero e um valor inesperado para negativos. Não há validação que impeça usos fora do contrato descrito, o que pode levar a resultados incorretos caso o método seja chamado inadvertidamente com valores inválidos.
Categoria: ausente (falta de validação do parâmetro)
Severidade: menor (não afeta o fluxo atual da classe, mas viola a especificação do contrato).

## L2 (cobre D2; FP na posição 1)

**Sugestão 1**

Linhas: 66-67
Descrição: O Javadoc de horasAdicionais especifica que o parâmetro minutosExcedentes deve ser maior que zero, porém o método aceita zero (ou valores negativos) e simplesmente calcula (minutosExcedentes + 59) / 60, retornando 0 para zero e um valor inesperado para negativos. Não há validação que impeça usos fora do contrato descrito, o que pode levar a resultados incorretos caso o método seja chamado inadvertidamente com valores inválidos.
Categoria: ausente (falta de validação do parâmetro)
Severidade: menor (não afeta o fluxo atual da classe, mas viola a especificação do contrato).

**Sugestão 2**

Linhas: 34-38
Descrição: A regra 4 estabelece que a tarifa nunca pode ultrapassar 3000 centavos, e o desconto (regra 5) deve ser aplicado depois desse limite. O método calcularTarifa nunca verifica nem impõe o teto de 3000, aplicando o desconto diretamente sobre o valor calculado, que pode ser maior que 3000. Por exemplo, para minutos = 1000 a tarifa calculada seria 800 + ( (1000-60+59)/60 )*300 = 800 + 16*300 = 5600, e o método retornaria 2800 após o desconto, violando o limite especificado.
Categoria: ausente
Severidade: maior
