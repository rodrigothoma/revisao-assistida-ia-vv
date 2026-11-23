/**
 * Calcula o frete de pedidos de uma loja virtual.
 * Todos os valores são expressos em centavos de real.
 */
public class CalculadoraFrete {

    /**
     * Calcula o valor do frete de um pedido com base no peso e no valor dos produtos.
     *
     * <p>Regras:</p>
     * <ol>
     *   <li>Promoção de frete grátis: pedidos com valor a partir de 20000 centavos,
     *       inclusive, têm tarifa zero.</li>
     *   <li>Pedidos com peso de até 1000 gramas, inclusive, pagam a tarifa fixa
     *       base de 1500 centavos.</li>
     *   <li>Acima de 1000 gramas, soma-se a tarifa base mais 300 centavos para
     *       cada bloco de 500 gramas adicionais ou fração.</li>
     *   <li>Garantia de frete máximo: o valor final cobrado não pode exceder
     *       o teto de 4500 centavos.</li>
     * </ol>
     *
     * @param pesoGramas peso total dos produtos, em gramas
     * @param valorPedido valor total dos produtos, em centavos
     * @return o valor do frete a ser cobrado, em centavos
     * @throws IllegalArgumentException se {@code pesoGramas} for menor ou igual a zero
     *         ou {@code valorPedido} for menor ou igual a zero
     */
    public int calcularFrete(int pesoGramas, int valorPedido) {
        validarDadosPedido(pesoGramas, valorPedido);
        if (valorPedido >= 20000) {
            return 0;
        }
        if (pesoGramas <= 1000) {
            return 1500;
        }
        int pesoExcedente = pesoGramas - 1000;
        int adicional = calcularAdicionalPeso(pesoExcedente);
        int total = 1500 + adicional;
        return Math.min(total, 4500);
    }

    /**
     * Valida se os parâmetros de entrada do pedido são válidos.
     *
     * @param pesoGramas peso em gramas
     * @param valorPedido valor do pedido em centavos
     */
    private void validarDadosPedido(int pesoGramas, int valorPedido) {
        if (pesoGramas <= 0) {
            throw new IllegalArgumentException("Peso deve ser maior que zero.");
        }
        if (valorPedido <= 0) {
            throw new IllegalArgumentException("Valor do pedido deve ser maior que zero.");
        }
    }

    /**
     * Calcula o valor adicional cobrado pelo excesso de peso além de 1000 gramas.
     *
     * @param pesoExcedente peso excedente em gramas
     * @return o valor adicional em centavos
     */
    private int calcularAdicionalPeso(int pesoExcedente) {
        int blocos = pesoExcedente / 500;
        if (pesoExcedente % 500 != 0) {
            blocos++;
        }
        return blocos * 300;
    }
}
