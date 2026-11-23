/**
 * Calcula a multa por atraso na devolução de livros de uma biblioteca universitária.
 * Todos os valores são expressos em centavos de real.
 */
public class CalculadoraMulta {

    /**
     * Calcula o valor da multa a ser cobrada pelo atraso na devolução de um exemplar.
     *
     * <p>Regras:</p>
     * <ol>
     *   <li>Atraso de até 3 dias, inclusive: multa de 200 centavos por dia de atraso.</li>
     *   <li>Atraso a partir de 4 dias: os 3 primeiros dias pagam a tarifa base
     *       de 200 centavos por dia e cada dia adicional subsequente paga
     *       350 centavos por dia.</li>
     *   <li>Exemplar de reserva técnica ({@code ehExemplarReserva} verdadeiro):
     *       o valor total da multa calculada é multiplicado por 2.</li>
     *   <li>Atraso superior a 120 dias ou menor ou igual a zero lança
     *       {@code IllegalArgumentException}.</li>
     * </ol>
     *
     * @param diasAtraso número de dias corridos em atraso
     * @param ehExemplarReserva indica se o exemplar pertence à reserva técnica
     * @return o valor total da multa a ser cobrada, em centavos
     * @throws IllegalArgumentException se {@code diasAtraso} for menor ou igual
     *         a zero ou superior a 120
     */
    public int calcularMulta(int diasAtraso, boolean ehExemplarReserva) {
        validarDiasAtraso(diasAtraso);
        int valorBase = calcularValorBase(diasAtraso);
        return aplicarRegraReserva(valorBase, ehExemplarReserva);
    }

    /**
     * Valida os limites permitidos para os dias de atraso.
     *
     * @param diasAtraso número de dias em atraso
     */
    private void validarDiasAtraso(int diasAtraso) {
        if (diasAtraso <= 0) {
            throw new IllegalArgumentException("Dias de atraso devem ser maiores que zero.");
        }
        if (diasAtraso > 120) {
            throw new IllegalArgumentException("Período máximo de atraso excedido.");
        }
    }

    /**
     * Calcula o valor base da multa antes da aplicação de eventuais multiplicadores.
     *
     * @param diasAtraso número de dias em atraso
     * @return o valor base da multa, em centavos
     */
    private int calcularValorBase(int diasAtraso) {
        if (diasAtraso <= 3) {
            return diasAtraso * 200;
        }
        return (3 * 200) + (diasAtraso * 350);
    }

    /**
     * Aplica o multiplicador caso o livro seja de reserva técnica.
     *
     * @param valorBase valor base da multa em centavos
     * @param ehExemplarReserva indicador de exemplar de reserva técnica
     * @return o valor final após aplicação da regra de reserva, em centavos
     */
    private int aplicarRegraReserva(int valorBase, boolean ehExemplarReserva) {
        if (ehExemplarReserva) {
            return (valorBase * 2) + 500;
        }
        return valorBase;
    }
}
