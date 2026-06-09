import os

# ==========================================================
# DADOS DO SISTEMA
# ==========================================================

cidades = {
    "São Paulo":     {"temperatura": 28, "chuva": 120, "vento": 45},
    "Rio de Janeiro":{"temperatura": 32, "chuva": 70,  "vento": 30},
    "Brasília":      {"temperatura": 25, "chuva": 40,  "vento": 20},
    "Salvador":      {"temperatura": 29, "chuva": 90,  "vento": 35},
    "Fortaleza":     {"temperatura": 31, "chuva": 140, "vento": 60}
}

historico_regioes = []

# Tupla com os níveis de alerta em ordem crescente de risco
niveis_alerta = ("VERDE", "AMARELO", "LARANJA", "VERMELHO")

# ==========================================================
# FUNÇÕES AUXILIARES
# ==========================================================

def pausar():
    """Aguarda ENTER e limpa a tela."""
    input("\nPressione ENTER para continuar...")
    os.system("cls" if os.name == "nt" else "clear")


def ler_numero(mensagem):
    """
    Solicita um número ao usuário com validação.

    Parâmetro: mensagem (str)
    Retorno: float
    """
    while True:
        try:
            return float(input(mensagem))
        except ValueError:
            print("Digite um número válido.")


def separador():
    """Imprime uma linha separadora."""
    print("=" * 60)

# ==========================================================
# CÁLCULO DE RISCO
# ==========================================================

def calcular_risco(chuva, vento):
    """
    Calcula o nível de risco com base na chuva e vento.
    Usa a tupla niveis_alerta para retornar o nível correto.

    Parâmetros: chuva (float), vento (float)
    Retorno: str — um dos valores de niveis_alerta
    """
    if chuva < 50 and vento < 30:
        return niveis_alerta[0]   # VERDE
    elif chuva < 100 and vento < 50:
        return niveis_alerta[1]   # AMARELO
    elif chuva < 150 and vento < 70:
        return niveis_alerta[2]   # LARANJA
    else:
        return niveis_alerta[3]   # VERMELHO


def calcular_chance(risco):
    """
    Retorna a chance de desastre (%) com base no nível de risco.

    Parâmetro: risco (str)
    Retorno: int
    """
    chances = {
        niveis_alerta[0]: 10,
        niveis_alerta[1]: 35,
        niveis_alerta[2]: 65,
        niveis_alerta[3]: 90
    }
    return chances[risco]

# ==========================================================
# EXIBIÇÃO
# ==========================================================

def exibir_local(nome, dados):
    """
    Exibe os dados climáticos e de risco de uma localidade.

    Parâmetros: nome (str), dados (dict)
    """
    risco = calcular_risco(dados["chuva"], dados["vento"])
    chance = calcular_chance(risco)

    separador()
    print(nome.upper())
    separador()
    print(f"Temperatura : {dados['temperatura']}°C")
    print(f"Chuva       : {dados['chuva']} mm")
    print(f"Vento       : {dados['vento']} km/h")
    print(f"\nNível de alerta  : {risco}")
    print(f"Chance de desastre: {chance}%")
    separador()

# ==========================================================
# MENUS / FUNCIONALIDADES
# ==========================================================

def descricao_projeto():
    """Exibe a descrição do projeto."""
    separador()
    print("NEOSPHERE — Descrição do Projeto")
    separador()
    print("Sistema de previsão climática e prevenção de desastres.")
    print("Monitora cidades brasileiras e permite cadastrar regiões")
    print("para análise automática de risco climático.")
    print("Utiliza dados de chuva e vento para calcular alertas")
    print(f"nos níveis: {', '.join(niveis_alerta)}.")
    separador()


def menu_cidades():
    """Exibe o menu de cidades e permite consultar cada uma."""
    lista = list(cidades.keys())

    while True:
        os.system("cls" if os.name == "nt" else "clear")
        separador()
        print("CIDADES DISPONÍVEIS")
        separador()
        for i, nome in enumerate(lista, 1):
            print(f"{i} - {nome}")
        print(f"{len(lista)+1} - Voltar")

        opcao = input("\nEscolha uma opção: ")

        if opcao.isdigit() and 1 <= int(opcao) <= len(lista):
            os.system("cls" if os.name == "nt" else "clear")
            nome = lista[int(opcao) - 1]
            exibir_local(nome, cidades[nome])
            pausar()
        elif opcao == str(len(lista) + 1):
            break
        else:
            print("Opção inválida.")
            pausar()


def adicionar_regiao():
    """Cadastra uma nova região com dados informados pelo usuário."""
    separador()
    print("CADASTRAR REGIÃO")
    separador()

    nome        = input("Nome da região: ")
    temperatura = ler_numero("Temperatura (°C): ")
    chuva       = ler_numero("Chuva (mm): ")
    vento       = ler_numero("Vento (km/h): ")

    risco  = calcular_risco(chuva, vento)
    chance = calcular_chance(risco)

    historico_regioes.append({
        "nome": nome, "temperatura": temperatura,
        "chuva": chuva, "vento": vento,
        "risco": risco, "chance": chance
    })

    print(f"\nRegião cadastrada! Nível: {risco} | Chance: {chance}%")


def exibir_historico():
    """Exibe todas as regiões cadastradas pelo usuário."""
    separador()
    print("HISTÓRICO DE REGIÕES")
    separador()

    if not historico_regioes:
        print("Nenhuma região cadastrada.")
        return

    for i, r in enumerate(historico_regioes, 1):
        print(f"\nREGIÃO {i} — {r['nome']}")
        print(f"  Temperatura: {r['temperatura']}°C | Chuva: {r['chuva']} mm | Vento: {r['vento']} km/h")
        print(f"  Alerta: {r['risco']} | Chance: {r['chance']}%")
    separador()


def relatorio_geral():
    """
    Gera relatório consolidado de todas as localidades monitoradas.
    Conta quantas estão em cada nível de alerta da tupla niveis_alerta.
    """
    contagem = {nivel: 0 for nivel in niveis_alerta}

    for cidade in cidades.values():
        contagem[calcular_risco(cidade["chuva"], cidade["vento"])] += 1

    for r in historico_regioes:
        contagem[r["risco"]] += 1

    separador()
    print("RELATÓRIO GERAL")
    separador()
    print(f"Cidades fixas    : {len(cidades)}")
    print(f"Regiões cadastradas: {len(historico_regioes)}")
    print()
    for nivel in niveis_alerta:
        print(f"  {nivel}: {contagem[nivel]}")
    separador()

# ==========================================================
# MENU PRINCIPAL
# ==========================================================

while True:
    os.system("cls" if os.name == "nt" else "clear")
    separador()
    print("NEOSPHERE — Sistema de Previsão Climática")
    separador()
    print("1 - Descrição do Projeto")
    print("2 - Cidades Disponíveis")
    print("3 - Adicionar Região")
    print("4 - Histórico de Regiões")
    print("5 - Relatório Geral")
    print("6 - Sair")

    match input("\nEscolha uma opção: "):
        case "1": os.system("cls" if os.name == "nt" else "clear"); descricao_projeto(); pausar()
        case "2": menu_cidades()
        case "3": os.system("cls" if os.name == "nt" else "clear"); adicionar_regiao(); pausar()
        case "4": os.system("cls" if os.name == "nt" else "clear"); exibir_historico(); pausar()
        case "5": os.system("cls" if os.name == "nt" else "clear"); relatorio_geral(); pausar()
        case "6": print("\nEncerrando sistema..."); break
        case _:   print("Opção inválida."); pausar()