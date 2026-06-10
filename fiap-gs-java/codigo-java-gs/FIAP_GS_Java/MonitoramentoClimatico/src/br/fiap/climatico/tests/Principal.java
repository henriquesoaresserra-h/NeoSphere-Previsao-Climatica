package br.fiap.climatico.tests;

import br.fiap.climatico.enums.NivelRisco;
import br.fiap.climatico.models.*;
import br.fiap.climatico.repository.ClimaticoRepository;
import br.fiap.climatico.service.ClimaticoService;
import br.fiap.climatico.service.UsuarioService;

import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Principal {

    public static void main(String[] args) {

        Scanner scanner = new Scanner(System.in);
        ClimaticoService service = new ClimaticoService();
        ClimaticoRepository repository = service.getRepository();
        UsuarioService usuarioService = new UsuarioService();

        System.out.println("===========================================");
        System.out.println("   SISTEMA DE MONITORAMENTO CLIMATICO");
        System.out.println("===========================================");
        System.out.println("  1. Login");
        System.out.println("  2. Cadastrar");
        System.out.println("-------------------------------------------");
        System.out.print("Opcao: ");
        String opcaoInicial = scanner.nextLine();

        if (opcaoInicial.equals("2")) {
            System.out.println("\n--- Cadastro ---");
            System.out.print("Nome: ");
            String nomeNovo = scanner.nextLine();
            System.out.print("Email: ");
            String emailNovo = scanner.nextLine();
            System.out.print("Senha: ");
            String senhaNova = scanner.nextLine();

            boolean cadastrado = usuarioService.cadastrar(nomeNovo, emailNovo, senhaNova);
            if (!cadastrado) {
                System.out.println("Nao foi possivel concluir o cadastro. Encerrando.");
                scanner.close();
                return;
            }
            System.out.println("Faca login para continuar.\n");
        }

        System.out.println("--- Login ---");
        System.out.print("Email: ");
        String emailDigitado = scanner.nextLine();
        System.out.print("Senha: ");
        String senhaDigitada = scanner.nextLine();

        Usuario usuarioLogado = usuarioService.autenticar(emailDigitado, senhaDigitada);

        if (usuarioLogado == null) {
            System.out.println("Email ou senha incorretos. Encerrando sistema.");
            scanner.close();
            return;
        }

        boolean ehAdmin = usuarioLogado instanceof Administrador;

        System.out.println("Bem-vindo(a), " + usuarioLogado.getNome() + "!");
        if (ehAdmin) {
            System.out.println("Perfil: Administrador");
        } else {
            System.out.println("Perfil: Usuario");
        }
        System.out.println();

        var dadoSP  = new DadoEstacao("Sao Paulo - SP",     "2025-06-10 14:00", 42.5, 18.0, 95.0, "Estacao Mirante",  "Automatica");
        var dadoCWB = new DadoEstacao("Curitiba - PR",       "2025-06-10 14:10", 28.0, 65.0, 25.0, "Estacao UFPR",     "Manual");
        var dadoRJ  = new DadoEstacao("Rio de Janeiro - RJ", "2025-06-10 14:20", 38.0, 35.0, 55.0, "Estacao Maracana", "Automatica");

        List<DadoEstacao> estacoes = new ArrayList<>(List.of(dadoSP, dadoCWB, dadoRJ));

        for (DadoEstacao dado : estacoes) {
            repository.salvarDado(dado);
            NivelRisco nivel = service.calcularRisco(dado);
            service.registrarAlerta(dado, nivel, dado.getDataHora());
        }

        String opcao = "";
        while (!opcao.equals("0")) {

            System.out.println("===========================================");
            System.out.println("   MENU PRINCIPAL");
            System.out.println("===========================================");
            System.out.println("  1. Ver estacoes monitoradas");
            System.out.println("  2. Ver todos os alertas");
            System.out.println("  3. Ver alertas por nivel de risco");
            if (ehAdmin) {
                System.out.println("  4. Cadastrar nova estacao  [Admin]");
            }
            System.out.println("  0. Sair");
            System.out.println("-------------------------------------------");
            System.out.print("Opcao: ");
            opcao = scanner.nextLine();

            if (opcao.equals("1")) {
                System.out.println("\n--- Estacoes monitoradas ---");
                for (int i = 0; i < estacoes.size(); i++) {
                    System.out.println("  " + (i + 1) + ". " + estacoes.get(i).getNomeEstacao()
                            + " - " + estacoes.get(i).getLocalizacao());
                }
                System.out.println("-------------------------------------------");
                System.out.print("Selecione uma estacao (ou 0 para voltar): ");
                String selecao = scanner.nextLine();

                if (!selecao.equals("0")) {
                    int indice = Integer.parseInt(selecao) - 1;
                    if (indice >= 0 && indice < estacoes.size()) {
                        DadoEstacao escolhida = estacoes.get(indice);
                        System.out.println("\n--- " + escolhida.getNomeEstacao() + " ---");
                        escolhida.exibirFichaTecnica();
                        NivelRisco risco = service.calcularRisco(escolhida);
                        System.out.println("  Risco    : " + risco);
                        // Busca e exibe o alerta correspondente a esta estacao
                        List<Alerta> alertasEstacao = service.getRepository().buscarAlertasPorNivel(risco);
                        for (Alerta a : alertasEstacao) {
                            if (a.getLocalizacao().equals(escolhida.getLocalizacao())) {
                                a.enviarAlerta();
                                break;
                            }
                        }
                    } else {
                        System.out.println("Estacao invalida.");
                    }
                }
                System.out.println();

            } else if (opcao.equals("2")) {
                System.out.println("\n--- Alertas registrados ---");
                service.listarAlertas();
                System.out.println();

            } else if (opcao.equals("3")) {
                System.out.println("\n--- Filtrar por nivel ---");
                System.out.println("  1. BAIXO");
                System.out.println("  2. MEDIO");
                System.out.println("  3. ALTO");
                System.out.println("  4. CRITICO");
                System.out.print("Opcao: ");
                String opcaoNivel = scanner.nextLine();

                NivelRisco nivelBusca;
                if (opcaoNivel.equals("4")) {
                    nivelBusca = NivelRisco.CRITICO;
                } else if (opcaoNivel.equals("3")) {
                    nivelBusca = NivelRisco.ALTO;
                } else if (opcaoNivel.equals("2")) {
                    nivelBusca = NivelRisco.MEDIO;
                } else {
                    nivelBusca = NivelRisco.BAIXO;
                }

                List<Alerta> encontrados = service.getRepository().buscarAlertasPorNivel(nivelBusca);
                System.out.println("\nAlertas nivel " + nivelBusca + ":");
                if (encontrados.isEmpty()) {
                    System.out.println("  Nenhum alerta encontrado.");
                } else {
                    encontrados.forEach(alerta -> System.out.println("  " + alerta));
                }
                System.out.println();

            } else if (opcao.equals("4")) {
                if (!ehAdmin) {
                    System.out.println("Acesso negado. Apenas administradores podem cadastrar estacoes.\n");
                } else {
                    System.out.println("\n--- Nova estacao ---");
                    System.out.print("Nome da estacao: ");
                    String nomeEst = scanner.nextLine();
                    System.out.print("Localizacao: ");
                    String local = scanner.nextLine();
                    System.out.print("Temperatura (C): ");
                    double temp = Double.parseDouble(scanner.nextLine());
                    System.out.print("Umidade (%): ");
                    double umidade = Double.parseDouble(scanner.nextLine());
                    System.out.print("Velocidade do vento (km/h): ");
                    double vento = Double.parseDouble(scanner.nextLine());

                    DadoEstacao novo = new DadoEstacao(local, "2025-06-10 15:00",
                            temp, umidade, vento, nomeEst, "Manual");

                    estacoes.add(novo);
                    service.receberDados(novo);
                    NivelRisco novoNivel = service.calcularRisco(novo);
                    Alerta novoAlerta = service.registrarAlerta(novo, novoNivel, "2025-06-10 15:01");

                    System.out.println("\nEstacao cadastrada:");
                    novo.exibirFichaTecnica();
                    System.out.println("  Risco    : " + novoNivel);
                    novoAlerta.enviarAlerta();
                    System.out.println();
                }

            } else if (!opcao.equals("0")) {
                System.out.println("Opcao invalida. Tente novamente.\n");
            }
        }

        System.out.println("Sistema encerrado. Ate logo, " + usuarioLogado.getNome() + "!");
        scanner.close();
    }
}
