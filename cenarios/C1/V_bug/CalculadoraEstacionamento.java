/**
 * Calcula a tarifa do estacionamento de um shopping.
 * Todos os valores são em centavos (800 significa R$ 8,00).
 */
public class CalculadoraEstacionamento {

    private static final int TARIFA_PRIMEIRA_HORA = 800;
    private static final int TARIFA_HORA_ADICIONAL = 300;

    /**
     * Calcula a tarifa a pagar por uma permanência.
     *
     * <p>Regras:</p>
     * <ol>
     *   <li>Permanências de até 15 minutos, inclusive, são gratuitas.</li>
     *   <li>Acima de 15 e até 60 minutos, inclusive, a tarifa é 800.</li>
     *   <li>Acima de 60 minutos, a tarifa é 800 mais 300 por hora adicional
     *       ou fração de hora.</li>
     *   <li>A tarifa de uma permanência nunca passa de 3000.</li>
     *   <li>Ticket validado por loja parceira paga metade da tarifa,
     *       arredondada para baixo. O desconto é aplicado depois do
     *       limite da regra 4.</li>
     * </ol>
     *
     * @param minutos  tempo de permanência, em minutos
     * @param validado {@code true} se o ticket foi validado por loja parceira
     * @return a tarifa, em centavos
     * @throws IllegalArgumentException se {@code minutos} for negativo
     */
    public int calcularTarifa(int minutos, boolean validado) {
        if (minutos < 0) {
            throw new IllegalArgumentException("minutos negativo: " + minutos);
        }
        int tarifa = tarifaPorTempo(minutos);
        if (validado) {
            tarifa = tarifa / 2;
        }
        return tarifa;
    }

    /**
     * Calcula a tarifa pelas regras 1 a 3 de
     * {@link #calcularTarifa(int, boolean)}, sem limite e sem desconto.
     *
     * @param minutos tempo de permanência, em minutos, não negativo
     * @return a tarifa, em centavos
     */
    private int tarifaPorTempo(int minutos) {
        if (minutos < 15) {
            return 0;
        }
        if (minutos <= 60) {
            return TARIFA_PRIMEIRA_HORA;
        }
        int horas = horasAdicionais(minutos - 60);
        return TARIFA_PRIMEIRA_HORA + horas * TARIFA_HORA_ADICIONAL;
    }

    /**
     * Converte os minutos além da primeira hora em horas adicionais,
     * contando a fração de hora como hora inteira.
     *
     * @param minutosExcedentes minutos além da primeira hora, maior que zero
     * @return o número de horas adicionais
     */
    private int horasAdicionais(int minutosExcedentes) {
        return (minutosExcedentes + 59) / 60;
    }
}
