/**
 * Testes internos do cenário C4 (só preparadores). Um teste por regra do Javadoc;
 * os marcados [GATILHO Dn] devem falhar em V_bug e passar em V_fix.
 */
public class TestesCalculadoraMulta {

    private static int falhas = 0;

    public static void main(String[] args) {
        CalculadoraMulta c = new CalculadoraMulta();

        igual("regra 1: 1 dia de atraso", 200, c.calcularMulta(1, false));
        igual("regra 1: 2 dias de atraso", 400, c.calcularMulta(2, false));
        igual("regra 1: 3 dias (inclusive)", 600, c.calcularMulta(3, false));
        igual("[GATILHO D1] regra 2: 5 dias de atraso (600 + 700)", 1300, c.calcularMulta(5, false));
        igual("[GATILHO D2] regra 3: 2 dias reserva tecnica (sem taxa extra)", 800, c.calcularMulta(2, true));
        lanca("exceção: dias zero", () -> c.calcularMulta(0, false));
        lanca("exceção: dias negativo", () -> c.calcularMulta(-5, false));
        lanca("exceção: dias acima de 120", () -> c.calcularMulta(121, false));

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
