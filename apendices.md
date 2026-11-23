# Material retirado do artigo

Os apêndices A e B do artigo foram retirados do corpo no Andamento 5 (24/11/2026), para caber no limite de páginas, e ficam aqui. A Declaração de Uso de IA, que era o Apêndice C, virou uma seção não numerada no fim do artigo.

## A. Instrução fornecida ao modelo

- **Modelo:** gpt-oss-120b (OpenAI, pesos abertos, Apache 2.0), identificador na API da Groq `openai/gpt-oss-120b`.
- **Data de execução:** 10 de novembro de 2026 (C1 a C4). A data e a hora de cada chamada estão no campo `data_hora` de cada JSON em `cenarios/<C>/sugestoes/`.
- **Configuração:** esforço de raciocínio `medium`; até 6.800 *tokens* de resposta; temperatura, *top-p* e demais parâmetros nos valores padrão da API; sem semente fixa (a semente que a Groq sorteou em cada chamada está em `resposta_completa.x_groq.seed`).

Cada instrução é enviada como instrução de sistema, seguida do código do cenário com linhas numeradas (`cenarios/<C>/<C>_numerado.txt` para V_bug e `<C>_fix_numerado.txt` para V_fix). A instrução restrita difere da usada no piloto com o Defects4J apenas na descrição do material (uma classe com Javadoc, sem testes), sem mudança no critério de defeito. A instrução genérica mantém o formato e retira a restrição a desvios do Javadoc. As instruções não foram alteradas depois do piloto com os cenários próprios.

- **Instrução restrita** (fonte das sugestões que apontam os defeitos e das medidas brutas): [`cenarios/prompt_sistema.txt`](cenarios/prompt_sistema.txt)
- **Instrução genérica** (fonte dos falsos positivos das listas): [`cenarios/prompt_generico.txt`](cenarios/prompt_generico.txt)

## B. Evidência de viabilidade

A viabilidade do estudo apoiou-se em três frentes.

- **Participantes:** os seis membros da equipe, quatro como revisores, atribuídos por sorteio às linhas do quadrado latino (Tabela 1 do artigo; ver `dados/sorteio.md`), e dois como preparadores. Todos são graduandos da mesma disciplina, origem que o artigo declara como ameaça à validade externa (Seção 4.6).
- **Instrumentos:** o piloto com o Defects4J foi executado e motivou a troca do objeto (Seção 4.2; material em `piloto/`). Os quatro cenários foram construídos, com V_fix, V_bug e testes gatilho verificados (`./cenarios/rodar_testes.sh C1` a `C4`). Os formulários e os roteiros foram gerados por script; estão em PDF em `formularios/`. O piloto com os cenários próprios, em 10 e 11 de novembro de 2026, mostrou que os formulários e os links pré-preenchidos funcionam e que os dois preparadores encontraram os oito defeitos, sem falsos positivos, levando de 5 a 21 minutos por cenário, tempo que é um limite inferior, pois sabiam que cada cenário tinha dois defeitos (respostas em `dados/piloto2/`).
- **Modelo:** o gpt-oss-120b foi acessado pela API da Groq com as instruções do item A. As quinze execuções por cenário usaram cerca de 34 mil *tokens* por cenário, com custo estimado de US$ 0,01 por cenário (`python3 piloto/unidades/custo_gemini.py cenarios`), e couberam na cota gratuita diária da API.
