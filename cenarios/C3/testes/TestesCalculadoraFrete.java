/**
 * Testes internos do cenário C3 (só preparadores). Um teste por regra do Javadoc;
 * os marcados [GATILHO Dn] devem falhar em V_bug e passar em V_fix.
 */
public class TestesCalculadoraFrete {

    private static int falhas = 0;

    public static void main(String[] args) {
        CalculadoraFrete c = new CalculadoraFrete();

        igual("regra 1: valor acima de 20000 tem frete grátis", 0, c.calcularFrete(500, 25000));
        igual("regra 1: peso grande mas valor acima de 20000 tem frete grátis", 0, c.calcularFrete(5000, 22000));
        igual("[GATILHO D1] regra 1: valor 20000 (inclusive) tem frete grátis", 0, c.calcularFrete(500, 20000));
        igual("regra 2: 500 g paga tarifa base 1500", 1500, c.calcularFrete(500, 10000));
        igual("regra 2: 1000 g (inclusive) paga tarifa base 1500", 1500, c.calcularFrete(1000, 10000));
        igual("regra 3: 1001 g paga 1500 + 1 fracao de 500 g", 1800, c.calcularFrete(1001, 10000));
        igual("regra 3: 1500 g paga 1500 + 1 bloco de 500 g", 1800, c.calcularFrete(1500, 10000));
        igual("regra 3: 1501 g paga 1500 + 2 fracoes de 500 g", 2100, c.calcularFrete(1501, 10000));
        igual("regra 3: 3000 g paga 1500 + 4 blocos de 500 g (abaixo do teto)", 2700, c.calcularFrete(3000, 5000));
        igual("[GATILHO D2] regra 4: 8000 g fica limitado ao teto de 4500", 4500, c.calcularFrete(8000, 5000));
        lanca("exceção: peso zero", () -> c.calcularFrete(0, 10000));
        lanca("exceção: peso negativo", () -> c.calcularFrete(-100, 10000));
        lanca("exceção: valor pedido zero", () -> c.calcularFrete(500, 0));
        lanca("exceção: valor pedido negativo", () -> c.calcularFrete(500, -5000));

        System.out.println(falhas == 0 ? "TODOS PASSARAM" : falhas + " FALHA(S)");
    }

    private static void igual(String nome, int esperado, int obtido) {
        if (esperado == obtido) {
            System.out.println("ok    " + nome);
        } else {
            falhas++;
            System.out.println("FALHA " + nome + " (esperado " + esperado + ", obtido " + obtido + ")");
        }
    }

    private static void lanca(String nome, Runnable r) {
        try {
            r.run();
            falhas++;
            System.out.println("FALHA " + nome + " (não lançou exceção)");
        } catch (IllegalArgumentException e) {
            System.out.println("ok    " + nome);
        }
    }
}
