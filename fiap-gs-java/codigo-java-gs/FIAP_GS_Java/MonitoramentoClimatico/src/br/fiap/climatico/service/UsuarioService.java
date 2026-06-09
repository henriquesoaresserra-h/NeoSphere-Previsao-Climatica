package br.fiap.climatico.service;

import br.fiap.climatico.models.Administrador;
import br.fiap.climatico.models.Usuario;

import java.util.ArrayList;
import java.util.List;

public class UsuarioService {

    private List<Usuario> usuarios = new ArrayList<>();
    private int contadorId = 1;

    public UsuarioService() {
        usuarios.add(new Usuario(contadorId++, "Joao Silva", "joao@email.com", "senha123"));
        usuarios.add(new Administrador(contadorId++, "Ana Admin", "ana@email.com", "admin456", 3));
    }

    public boolean cadastrar(String nome, String email, String senha) {
        for (Usuario u : usuarios) {
            if (u.getEmail().equals(email)) {
                System.out.println("Email ja cadastrado no sistema.");
                return false;
            }
        }
        Usuario novo = new Usuario(contadorId++, nome, email, senha);
        usuarios.add(novo);
        System.out.println("Cadastro realizado com sucesso! Bem-vindo(a), " + nome + ".");
        return true;
    }

    public Usuario autenticar(String email, String senha) {
        for (Usuario u : usuarios) {
            if (u.autenticar(email, senha)) {
                return u;
            }
        }
        return null;
    }

    public List<Usuario> getUsuarios() {
        return usuarios;
    }

    public void setUsuarios(List<Usuario> usuarios) {
        this.usuarios = usuarios;
    }
}
