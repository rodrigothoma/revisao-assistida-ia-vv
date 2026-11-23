/**
 * Testes internos do cenário C1 (só preparadores). Um teste por regra do Javadoc;
 * os marcados [GATILHO Dn] devem falhar em V_bug e passar em V_fix.
 */
public class TestesCalculadoraEstacionamento {

    private static int falhas = 0;

    public static void main(String[] args) {
        CalculadoraEstacionamento c = new CalculadoraEstacionamento();

        igual("regra 1: 0 min é grátis", 0, c.calcularTarifa(0, false));
        igual("regra 1: 10 min é grátis", 0, c.calcularTarifa(10, false));
        igual("[GATILHO D1] regra 1: 15 min (inclusive) é grátis", 0, c.calcularTarifa(15, false));
        igual("regra 2: 16 min paga 800", 800, c.calcularTarifa(16, false));
        igual("regra 2: 60 min (inclusive) paga 800", 800, c.calcularTarifa(60, false));
        igual("regra 3: 61 min paga 800 + 1 hora", 1100, c.calcularTarifa(61, false));
        igual("regra 3: 120 min paga 800 + 1 hora", 1100, c.calcularTarifa(120, false));
        igual("regra 3: 121 min paga 800 + 2 horas", 1400, c.calcularTarifa(121, false));
        igual("regra 3: 480 min paga 800 + 7 horas (abaixo do limite)", 2900, c.calcularTarifa(480, false));
        igual("[GATILHO D2] regra 4: 600 min fica limitado a 3000", 3000, c.calcularTarifa(600, false));
        igual("regra 5: 61 min validado paga metade", 550, c.calcularTarifa(61, true));
        igual("regra 5: 16 min validado paga metade", 400, c.calcularTarifa(16, true));
        igual("[GATILHO D2] regra 5: desconto depois do limite (600 min validado)", 1500, c.calcularTarifa(600, true));
        lanca("exceção: minutos negativo", () -> c.calcularTarifa(-1, false));

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
