package br.fiap.climatico.models;

import br.fiap.climatico.enums.NivelRisco;
public class DadoEstacao extends DadoClimatico {

    private String nomeEstacao;
    private String tipoEstacao;

    public DadoEstacao() {
        super();
    }

    public DadoEstacao(String localizacao, String dataHora, double temperatura,
                       double umidade, double velocidadeVento,
                       String nomeEstacao, String tipoEstacao) {
        super(localizacao, dataHora, temperatura, umidade, velocidadeVento);
        this.nomeEstacao = nomeEstacao;
        this.tipoEstacao = tipoEstacao;
    }

    @Override
    public void exibirFichaTecnica() {
        System.out.println("  Estacao  : " + nomeEstacao + " (" + tipoEstacao + ")");
        System.out.println("  Local    : " + getLocalizacao());
        System.out.println("  Data/Hora: " + getDataHora());
        System.out.println("  Temp     : " + temperatura + "C");
        System.out.println("  Umidade  : " + umidade + "%");
        System.out.println("  Vento    : " + velocidadeVento + " km/h");
    }

    @Override
    public NivelRisco calcularNivelRisco() {
        int pontuacao = 0;

        if (temperatura >= 40) {
            pontuacao += 3;
        } else if (temperatura >= 35) {
            pontuacao += 2;
        } else if (temperatura >= 30) {
            pontuacao += 1;
        }

        if (umidade <= 20) {
            pontuacao += 3;
        } else if (umidade <= 40) {
            pontuacao += 2;
        } else if (umidade <= 60) {
            pontuacao += 1;
        }

        if (velocidadeVento >= 90) {
            pontuacao += 3;
        } else if (velocidadeVento >= 60) {
            pontuacao += 2;
        } else if (velocidadeVento >= 40) {
            pontuacao += 1;
        }

        if (pontuacao >= 7) {
            return NivelRisco.CRITICO;
        } else if (pontuacao >= 5) {
            return NivelRisco.ALTO;
        } else if (pontuacao >= 3) {
            return NivelRisco.MEDIO;
        } else {
            return NivelRisco.BAIXO;
        }
    }

    public String getNomeEstacao() {
        return nomeEstacao;
    }

    public void setNomeEstacao(String nomeEstacao) {
        this.nomeEstacao = nomeEstacao;
    }

    public String getTipoEstacao() {
        return tipoEstacao;
    }

    public void setTipoEstacao(String tipoEstacao) {
        this.tipoEstacao = tipoEstacao;
    }

    @Override
    public String toString() {
        return nomeEstacao + " | " + getLocalizacao()
                + " | Temp: " + temperatura + "C"
                + " | Umidade: " + umidade + "%"
                + " | Vento: " + velocidadeVento + "km/h";
    }
}
