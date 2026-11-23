# Listas de sugestões — C4 (não compartilhar com os revisores)

Modelo: openai/gpt-oss-120b (Groq), raciocínio medium. Gerado em 10/11/2026.
Texto literal do modelo; só foram removidos a numeração, a marcação Markdown (`**` e crases) e os hífens não separáveis.

Regra de escolha (Seção 4.3 do artigo, "Listas de sugestões"): o VP é a primeira sugestão das execuções com o prompt restrito em V_bug que atende à regra de correspondência e cujo exemplo numérico, se houver, está correto; o FP é o primeiro apontamento das execuções com o prompt genérico em V_fix classificado como FP (apontamentos sobre documentação ou que são outro achado real são pulados).

Origem: VP de D1 = `restrito/C4_numerado_exec1.txt, item 1`; VP de D2 = `restrito/C4_numerado_exec1.txt, item 2`; FP = `generico/C4_fix_numerado_exec1.txt, item 2`.

## L1 (cobre D1; FP na posição 2)

**Sugestão 1**

Linhas: 58
Descrição: O cálculo do valor base para atrasos superiores a 3 dias está incorreto. O código soma (diasAtraso * 350), aplicando a tarifa de 350 centavos a todos os dias, quando a especificação exige que apenas os dias adicionais (a partir do 4º) sejam cobrados a 350 centavos, mantendo os 3 primeiros a 200 centavos cada. Exemplo que evidencia o erro: diasAtraso = 5 deve resultar em 3*200 + 2*350 = 1300 centavos, mas o método devolve 5*350 + 600 = 2350 centavos.
Categoria: incorreto
Severidade: maior

**Sugestão 2**

Linhas: 54-59
Descrição: O cálculo do valor base utiliza números mágicos (200, 350 e 3) sem definição de constantes nomeadas, dificultando a manutenção e a compreensão das regras de negócio.
Categoria: ausente
Severidade: menor

## L2 (cobre D2; FP na posição 1)

**Sugestão 1**

Linhas: 54-59
Descrição: O cálculo do valor base utiliza números mágicos (200, 350 e 3) sem definição de constantes nomeadas, dificultando a manutenção e a compreensão das regras de negócio.
Categoria: ausente
Severidade: menor

**Sugestão 2**

Linhas: 70
Descrição: Na aplicação da regra de reserva técnica o método adiciona 500 centavos ao resultado ((valorBase * 2) + 500), porém a especificação indica apenas a multiplicação por 2 do valor total calculado, sem nenhum acréscimo adicional. Exemplo: para valorBase = 1000 e ehExemplarReserva = true, o método devolve 2500 centavos, enquanto o esperado é 2000 centavos.
Categoria: incorreto
Severidade: maior
