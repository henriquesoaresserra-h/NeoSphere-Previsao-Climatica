[README (3).md](https://github.com/user-attachments/files/29111287/README.3.md)
# 🌍 NeoSphere — Previsão Climática & Prevenção de Desastres

> Sistema integrado de monitoramento climático e prevenção de desastres naturais desenvolvido para a **Global Solution — FIAP 2026**.

---

## Sobre o Projeto

O **NeoSphere** é uma plataforma completa que combina análise de dados climáticos em tempo real, banco de dados robusto, interface web responsiva e suporte automatizado por inteligência artificial — tudo com o objetivo de mitigar os impactos de desastres naturais.

O projeto foi desenvolvido de forma colaborativa por cinco integrantes, cada um responsável por uma frente técnica específica. Este repositório centraliza o ecossistema completo para fins de portfólio e apresentação acadêmica.

---

## 👥 Equipe & Contribuições

| Integrante | RM | Turma | Frente | Responsabilidades |
|---|---|---|---|---|
| **[Henrique Soares Serra](https://www.linkedin.com/in/henrique-s-s-47419a3aa/)** — *Líder do Projeto* | 573618 | 1TDSPI | Banco de Dados | Coordenação geral da equipe e divisão de frentes; modelagem conceitual, lógica e física do banco; scripts SQL; documentação do BD; contribuição na arquitetura de software |
| **Lucas Costa** | 571016 | 1TDSPI | Front-End | Interface web responsiva e moderna; integração com as APIs do sistema |
| **Christian Pereira Rodrigues** | 571586 | 1TDSPJ | Back-End Java | Arquitetura da API REST; lógica de negócio; padrões de projeto; integração com o banco de dados |
| **[Arthur Chang Skolimoski](https://www.linkedin.com/in/arthur-chang-skolimoski-750598397/)** | 572510 | 1TDSPH | Python & Dados | Scripts de análise e processamento de dados climáticos; automações do sistema |
| **Lucas Fortunato Brandão de Pinho** | 572860 | 1TDSPI | IA & Chatbot | Desenvolvimento do chatbot assistente; integração do módulo de inteligência artificial |

> **Nota:** A modelagem de software e documentação de arquitetura (`/software`) foi uma contribuição coletiva da equipe.

---

## 🗂️ Estrutura do Repositório

```
NeoSphere-Previsao-Climatica/
│
├── GS-Front-End/
│   ├── GSFront/                        # Código-fonte da interface web
│   └── images/                         # Assets visuais do front-end
│
├── GS_Database/
│   ├── neosphere_script.sql            # Script de criação e população do banco
│   ├── modelo MER.png                  # Modelo Entidade-Relacionamento
│   └── modelo lógico.png               # Modelo lógico do banco de dados
│
├── fiap-gs-java/
│   ├── codigo-java-gs/                 # Código-fonte da API REST em Java
│   └── documentacao-gs-java.pdf        # Documentação técnica do back-end
│
├── gs-chatbot/
│   ├── Global-Solution-dialog.json     # Fluxo de diálogo do chatbot
│   └── flowsgs.json                    # Fluxo de automação
│
├── python/
│   ├── GOBAL-python.py                 # Script principal de análise de dados
│   └── GS-python.pdf                   # Documentação do módulo Python
│
└── software/
    ├── figma/                          # Arquivos de design da interface
    ├── Business Model Canvas.jpg       # Canvas do modelo de negócio
    └── GLOBAL SOLUTION 2026.pdf        # Documentação geral do projeto
```

---

## 🛠️ Tecnologias Utilizadas

| Camada | Tecnologias |
|---|---|
| Back-End | Java |
| Banco de Dados | Oracle SQL |
| Front-End | HTML5, CSS3, JavaScript |
| IA & Dados | Python |
| Chatbot | Python + IA |
| Documentação | Modelagem UML / Software Design |

---

## Como Executar

**Pré-requisitos:** JDK instalado, Python 3.x e acesso a um banco Oracle.

1. Clone o repositório
   ```bash
   git clone https://github.com/henriquesoaresserra-h/NeoSphere-Previsao-Climatica
   ```

2. **Back-End Java** — acesse `fiap-gs-java/` e execute a aplicação conforme as instruções internas do módulo.

3. **Banco de Dados** — acesse `GS_Database/` e execute os scripts SQL na sequência indicada na documentação interna.

4. **Front-End** — abra os arquivos de `GS-Front-End/` diretamente no navegador ou sirva com um servidor local.

5. **Python & Chatbot** — acesse `python/` e `gs-chatbot/` e instale as dependências com `pip install -r requirements.txt` antes de executar.

---

*Projeto acadêmico desenvolvido para a Global Solution — FIAP, 2026.*
