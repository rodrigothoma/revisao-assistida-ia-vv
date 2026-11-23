# Exemplo do roteiro (só leitura, não é medido)

Imagem: `exemplo.png` (gerada de `Eleitor.java`).

## Sugestão recebida (como aparece nos cenários com sugestões)

**Sugestão 1**
Linhas: 15
Descrição: o Javadoc diz que o voto é obrigatório de 18 a 70 anos, inclusive, mas a condição `idade < 70` exclui 70. Para idade = 70, o método retorna false.
Categoria: incorreto
Severidade: maior

## Como seria o preenchimento

- **Sugestão 1:** Aceito. Justificativa: "o Javadoc diz inclusive, e 70 fica de fora". (Caso julgasse que a sugestão não aponta um defeito funcional frente ao Javadoc, escolheria "Descarto" e justificaria).
- **Encontrou algum defeito?** Sim.
- **Apontamento 1:**
  - Linhas: `15`
  - Descrição: "Com idade 70, retorna false; o Javadoc diz que de 18 a 70, inclusive, o voto é obrigatório."
  - Categoria: Incorreto
  - Severidade: Maior
  - Origem: Sugestão 1
- **Registrar outro apontamento?** Não → Enviar.

Num cenário sem sugestões, o preenchimento é o mesmo, só sem a página de sugestões e sem o campo Origem.
