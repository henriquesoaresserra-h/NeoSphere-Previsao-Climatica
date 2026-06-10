package br.fiap.climatico.models;

public class Administrador extends Usuario {

    private int nivelAcesso;

    public Administrador() {
        super();
    }

    public Administrador(int id, String nome, String email, String senha, int nivelAcesso) {
        super(id, nome, email, senha);
        this.nivelAcesso = nivelAcesso;
    }

    @Override
    public String toString() {
        return "Administrador{" +
                "id=" + getId() +
                ", nome='" + getNome() + '\'' +
                ", email='" + getEmail() + '\'' +
                ", nivelAcesso=" + nivelAcesso +
                '}';
    }

    public void gerenciarRegras(String descricaoRegra) {
        if (nivelAcesso >= 2) {
            System.out.println("Administrador [" + getNome() + "] criou nova regra: " + descricaoRegra);
        } else {
            System.out.println("Nivel de acesso insuficiente para gerenciar regras.");
        }
    }

    public int getNivelAcesso() {
        return nivelAcesso;
    }

    public void setNivelAcesso(int nivelAcesso) {
        this.nivelAcesso = nivelAcesso;
    }
}
