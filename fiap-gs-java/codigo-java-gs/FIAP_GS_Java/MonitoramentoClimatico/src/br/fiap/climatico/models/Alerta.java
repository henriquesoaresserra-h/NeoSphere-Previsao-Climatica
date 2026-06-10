package br.fiap.climatico.models;

import br.fiap.climatico.enums.NivelRisco;
import br.fiap.climatico.interfaces.Alertavel;

public class Alerta implements Alertavel {

    private int id;
    private String mensagem;
    private NivelRisco nivel;
    private String localizacao;
    private String dataHora;

    public Alerta() {}

    public Alerta(int id, String mensagem, NivelRisco nivel,
                  String localizacao, String dataHora) {
        this.id = id;
        this.mensagem = mensagem;
        this.nivel = nivel;
        this.localizacao = localizacao;
        this.dataHora = dataHora;
    }

    @Override
    public void enviarAlerta() {
        System.out.println("-------------------------------------------");
        System.out.println("  NOTIFICACAO DE ALERTA CLIMATICO");
        System.out.println("  ID       : " + id);
        System.out.println("  Nivel    : " + nivel);
        System.out.println("  Local    : " + localizacao);
        System.out.println("  Mensagem : " + mensagem);
        System.out.println("  Data/Hora: " + dataHora);
        System.out.println("  [Notificando front-end e chatbot...]");
        System.out.println("-------------------------------------------");
    }

    @Override
    public String gerarMensagem() {
        return nivel + " | " + localizacao + " - " + mensagem;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getMensagem() {
        return mensagem;
    }

    public void setMensagem(String mensagem) {
        this.mensagem = mensagem;
    }

    public NivelRisco getNivel() {
        return nivel;
    }

    public void setNivel(NivelRisco nivel) {
        this.nivel = nivel;
    }

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

    @Override
    public String toString() {
        return "Alerta #" + id + " | " + nivel + " | " + localizacao + " | " + dataHora;
    }
}
