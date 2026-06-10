package br.fiap.climatico.service;

import br.fiap.climatico.enums.NivelRisco;
import br.fiap.climatico.models.Alerta;
import br.fiap.climatico.models.DadoEstacao;

import br.fiap.climatico.repository.ClimaticoRepository;

import java.util.ArrayList;
import java.util.List;

public class ClimaticoService {

    private List<Alerta> alertas = new ArrayList<>();
    private ClimaticoRepository repository = new ClimaticoRepository();
    private int contadorAlerta = 1;

    public void receberDados(DadoEstacao dado) {
        repository.salvarDado(dado);
        System.out.println("-------------------------------------------");
        System.out.println("  DADOS RECEBIDOS DA API EXTERNA");
        System.out.println("  Estacao  : " + dado.getNomeEstacao());
        System.out.println("  Local    : " + dado.getLocalizacao());
        System.out.println("  Data/Hora: " + dado.getDataHora());
        System.out.println("  [Dado salvo no banco de dados...]");
        System.out.println("-------------------------------------------");
    }

    public NivelRisco calcularRisco(DadoEstacao dado) {
        return dado.calcularNivelRisco();
    }

    public Alerta registrarAlerta(DadoEstacao dado, NivelRisco nivel, String dataHora) {
        String mensagem = "Temp " + dado.getTemperatura() + "C  "
                + "Umidade " + dado.getUmidade() + "%  "
                + "Vento " + dado.getVelocidadeVento() + "km/h";

        Alerta alerta = new Alerta(contadorAlerta++, mensagem, nivel,
                dado.getLocalizacao(), dataHora);

        alertas.add(alerta);
        repository.salvarAlerta(alerta);
        return alerta;
    }

    public void listarAlertas() {
        for (int i = 0; i < alertas.size(); i++) {
            alertas.get(i).enviarAlerta();
        }
    }

    public void exibirAlertasAtivos() {
        for (Alerta alerta : alertas) {
            if (alerta.getNivel() == NivelRisco.ALTO || alerta.getNivel() == NivelRisco.CRITICO) {
                alerta.enviarAlerta();
            }
        }
    }

    public List<Alerta> getAlertas() {
        return alertas;
    }

    public void setAlertas(List<Alerta> alertas) {
        this.alertas = alertas;
    }

    public ClimaticoRepository getRepository() {
        return repository;
    }

    public void setRepository(ClimaticoRepository repository) {
        this.repository = repository;
    }
}
