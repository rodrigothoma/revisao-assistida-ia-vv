/**
 * Regras de obrigatoriedade do voto.
 */
public class Eleitor {

    /**
     * Informa se o voto é obrigatório para uma pessoa.
     *
     * <p>O voto é obrigatório para quem tem de 18 a 70 anos, inclusive.</p>
     *
     * @param idade idade da pessoa, em anos
     * @return {@code true} se o voto for obrigatório
     */
    public boolean votoObrigatorio(int idade) {
        return idade >= 18 && idade < 70;
    }
}
