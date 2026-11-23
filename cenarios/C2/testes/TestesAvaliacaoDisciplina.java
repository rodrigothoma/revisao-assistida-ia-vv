/**
 * Testes internos do cenário C2 (só preparadores). Um teste por regra do Javadoc;
 * os marcados [GATILHO Dn] devem falhar em V_bug e passar em V_fix.
 */
public class TestesAvaliacaoDisciplina {

    private static int falhas = 0;

    public static void main(String[] args) {
        AvaliacaoDisciplina a = new AvaliacaoDisciplina();

        igual("média: pesos 3, 3 e 4", 70, a.calcularMedia(70, 70, 70));
        igual("média: divisão inteira (58,4 vira 58)", 58, a.calcularMedia(61, 55, 59));
        igual("média: P1 maior que P2", 64, a.calcularMedia(80, 40, 70));
        igual("[GATILHO D2] média: P2 maior que P1 não substitui a P1", 64, a.calcularMedia(40, 80, 70));
        igual("situação: frequência 74 é REPROVADO_FREQUENCIA (média baixa)", "REPROVADO_FREQUENCIA", a.situacao(30, 30, 30, 74).name());
        igual("[GATILHO D1] situação: frequência 60 com média 80 é REPROVADO_FREQUENCIA", "REPROVADO_FREQUENCIA", a.situacao(80, 80, 80, 60).name());
        igual("situação: média 60 com frequência 75 é APROVADO", "APROVADO", a.situacao(60, 60, 60, 75).name());
        igual("situação: média 59 é EXAME", "EXAME", a.situacao(80, 50, 50, 90).name());
        igual("situação: média 40 é EXAME", "EXAME", a.situacao(40, 40, 40, 100).name());
        igual("situação: média 39 é REPROVADO", "REPROVADO", a.situacao(50, 30, 37, 100).name());
        lanca("exceção: nota acima de 100", () -> a.calcularMedia(101, 50, 50));
        lanca("exceção: nota negativa", () -> a.calcularMedia(50, 50, -1));
        lanca("exceção: frequência acima de 100", () -> a.situacao(50, 50, 50, 101));
        lanca("exceção: frequência negativa", () -> a.situacao(50, 50, 50, -1));

        System.out.println(falhas == 0 ? "TODOS PASSARAM" : falhas + " FALHA(S)");
    }

    private static void igual(String nome, Object esperado, Object obtido) {
        if (esperado.equals(obtido)) {
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
