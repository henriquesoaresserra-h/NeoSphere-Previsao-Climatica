package br.fiap.climatico.models;

import br.fiap.climatico.enums.NivelRisco;
public abstract class DadoClimatico {

    private String localizacao;
    private String dataHora;
    protected double temperatura;
    protected double umidade;
    protected double velocidadeVento;

    public void exibirFichaTecnica() {
        System.out.println("Local: " + localizacao);
        System.out.println("Data/Hora: " + dataHora);
        System.out.println("Temperatura: " + temperatura + "°C");
        System.out.println("Umidade: " + umidade + "%");
        System.out.println("Vento: " + velocidadeVento + " km/h");
    }

    public DadoClimatico() {}

    public DadoClimatico(String localizacao, String dataHora, double temperatura,
                         double umidade, double velocidadeVento) {
        this.localizacao = localizacao;
        this.dataHora = dataHora;
        this.temperatura = temperatura;
        this.umidade = umidade;
        this.velocidadeVento = velocidadeVento;
    }

    public abstract NivelRisco calcularNivelRisco();

    // Métodos de acesso
    public String getLocalizacao() {
        return localizacao;
    }

    public void setLocalizacao(String localizacao) {
        this.localizacao = localizacao;
    }

    public String getDataHora() {
        return dataHora;
    }

    public void setDataHora(String dataHora) {
        this.dataHora = dataHora;
    }

    public double getTemperatura() {
        return temperatura;
    }

    public void setTemperatura(double temperatura) {
        this.temperatura = temperatura;
    }

    public double getUmidade() {
        return umidade;
    }

    public void setUmidade(double umidade) {
        this.umidade = umidade;
    }

    public double getVelocidadeVento() {
        return velocidadeVento;
    }

    public void setVelocidadeVento(double velocidadeVento) {
        this.velocidadeVento = velocidadeVento;
    }
}
