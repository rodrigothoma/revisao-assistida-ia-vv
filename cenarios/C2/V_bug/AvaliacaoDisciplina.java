/**
 * Calcula a média e a situação final dos alunos de uma disciplina.
 * As notas são em décimos de ponto, de 0 a 100 (75 significa 7,5).
 */
public class AvaliacaoDisciplina {

    /** Situação final do aluno na disciplina. */
    public enum Situacao { APROVADO, EXAME, REPROVADO, REPROVADO_FREQUENCIA }

    /**
     * Calcula a média final do aluno.
     *
     * <p>A média é (3 × p1 + 3 × p2 + 4 × trabalho) / 10, com divisão
     * inteira: a parte fracionária é descartada.</p>
     *
     * @param p1       nota da primeira prova, de 0 a 100
     * @param p2       nota da segunda prova, de 0 a 100
     * @param trabalho nota do trabalho, de 0 a 100
     * @return a média, de 0 a 100
     * @throws IllegalArgumentException se alguma nota estiver fora de 0 a 100
     */
    public int calcularMedia(int p1, int p2, int trabalho) {
        validarNota(p1);
        validarNota(p2);
        validarNota(trabalho);
        if (p2 > p1) {
            p1 = p2;
        }
        return (3 * p1 + 3 * p2 + 4 * trabalho) / 10;
    }

    /**
     * Define a situação final do aluno a partir das notas e da frequência.
     *
     * <p>Regras, em ordem de prioridade:</p>
     * <ol>
     *   <li>Frequência abaixo de 75% resulta em REPROVADO_FREQUENCIA,
     *       qualquer que seja a média.</li>
     *   <li>Média a partir de 60 resulta em APROVADO.</li>
     *   <li>Média de 40 a 59 resulta em EXAME.</li>
     *   <li>Média abaixo de 40 resulta em REPROVADO.</li>
     * </ol>
     *
     * @param p1         nota da primeira prova, de 0 a 100
     * @param p2         nota da segunda prova, de 0 a 100
     * @param trabalho   nota do trabalho, de 0 a 100
     * @param frequencia frequência do aluno, em porcentagem, de 0 a 100
     * @return a situação final
     * @throws IllegalArgumentException se alguma nota ou a frequência
     *         estiver fora de 0 a 100
     */
    public Situacao situacao(int p1, int p2, int trabalho, int frequencia) {
        if (frequencia < 0 || frequencia > 100) {
            throw new IllegalArgumentException("frequencia invalida: " + frequencia);
        }
        int media = calcularMedia(p1, p2, trabalho);
        if (media >= 60) {
            return Situacao.APROVADO;
        }
        if (frequencia < 75) {
            return Situacao.REPROVADO_FREQUENCIA;
        }
        if (media >= 40) {
            return Situacao.EXAME;
        }
        return Situacao.REPROVADO;
    }

    /**
     * Verifica se uma nota está entre 0 e 100, inclusive.
     *
     * @param nota a nota a verificar
     * @throws IllegalArgumentException se a nota estiver fora de 0 a 100
     */
    private void validarNota(int nota) {
        if (nota < 0 || nota > 100) {
            throw new IllegalArgumentException("nota invalida: " + nota);
        }
    }
}
