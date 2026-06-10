package br.fiap.climatico.repository;

import br.fiap.climatico.enums.NivelRisco;
import br.fiap.climatico.models.Alerta;
import br.fiap.climatico.models.DadoEstacao;


import java.util.ArrayList;
import java.util.List;

public class ClimaticoRepository {

    private List<DadoEstacao> dados = new ArrayList<>();
    private List<Alerta> alertas = new ArrayList<>();

    public void salvarDado(DadoEstacao dado) {
        dados.add(dado);
    }

    public void salvarAlerta(Alerta alerta) {
        alertas.add(alerta);
    }

    public List<DadoEstacao> buscarTodosDados() {
        return dados;
    }

    public List<Alerta> buscarAlertasPorNivel(NivelRisco nivel) {
        List<Alerta> resultado = new ArrayList<>();
        for (Alerta alerta : alertas) {
            if (alerta.getNivel() == nivel) {
                resultado.add(alerta);
            }
        }
        return resultado;
    }

    public List<DadoEstacao> getDados() {
        return dados;
    }

    public void setDados(List<DadoEstacao> dados) {
        this.dados = dados;
    }

    public List<Alerta> getAlertas() {
        return alertas;
    }

    public void setAlertas(List<Alerta> alertas) {
        this.alertas = alertas;
    }
}
