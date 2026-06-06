import datetime

# Lista global que armazenará os dados inseridos pelo usuário
dados_climaticos = []


def coletar_dados_input():
    """Interface de terminal para o usuário digitar os dados diários."""
    print("=" * 55)
    print("    SISTEMA INTERATIVO DE COLETA DE DADOS CLIMÁTICOS    ")
    print("Este Programa serve para coletar os dados climaticos e gerar uma reportagem de riscos de acordo com os dias anteriores.")
    print("=" * 55)
    print("Digite os dados dia após dia. Quando quiser parar de inserir as caracteristicas do dia ou encerrar, digite 'sair'.\n")

    contador = 1
    while True:
        print(f"--- Dados do Dia #{contador} ---")

        # Entrada da Data
        data_input = input(
            "Data (AAAA-MM-DD) [Deixe em branco para usar a data de hoje]: "
        ).strip()
        if data_input.lower() == "sair":
            break
        if not data_input:
            data_input = str(datetime.date.today())

        # Entrada da Temperatura
        try:
            temp_raw = input("Temperatura Média (°C): ").strip()
            if temp_raw.lower() == "sair":
                break
            temp = float(temp_raw)

            # Entrada da Umidade
            umi_raw = input("Umidade Relativa do Ar (%): ").strip()
            if umi_raw.lower() == "sair":
                break
            umidade = float(umi_raw)
            if not (0 <= umidade <= 100):
                print(
                    "❌ Erro: A umidade deve ser entre 0% e 100%. Reinicie este dia."
                )
                continue

            # Entrada da Chuva
            chuva_raw = input("Volume de Chuva (mm): ").strip()
            if chuva_raw.lower() == "sair":
                break
            chuva = float(chuva_raw)
            if chuva < 0:
                print(
                    "❌ Erro: O volume de chuva não pode ser negativo. Reinicie este dia."
                )
                continue

        except ValueError:
            print(
                "❌ Erro: Por favor, insira valores numéricos válidos para temperatura, umidade e chuva.\n"
            )
            continue

        # Salvando os dados validados no nosso "banco de dados" temporário
        dados_climaticos.append(
            {"data": data_input, "temp": temp, "umidade": umidade, "chuva": chuva}
        )
        print("✅ Dados do dia registrados com sucesso!\n")
        contador += 1

    print("\nColeta finalizada. Gerando relatórios...\n")


def analisar_historico(dados):
    """Calcula estatísticas básicas dos dados fornecidos."""
    total_dias = len(dados)
    if total_dias == 0:
        return None

    soma_temp = sum(d["temp"] for d in dados)
    soma_umi = sum(d["umidade"] for d in dados)
    total_chuva = sum(d["chuva"] for d in dados)
    temps = [d["temp"] for d in dados]

    return {
        "media_temp": soma_temp / total_dias,
        "media_umi": soma_umi / total_dias,
        "total_chuva": total_chuva,
        "temp_max": max(temps),
        "temp_min": min(temps),
    }


def prever_proximo_dia(dados):
    """Gera uma previsão simples baseada na tendência dos últimos dias."""
    if len(dados) < 2:
        return "Dados insuficientes (mínimo de 2 dias) para projetar uma tendência."

    # Se tiver 3 ou mais dias, usa os 3 últimos. Se tiver 2, usa os 2.
    ultimos_dias = dados[-3:] if len(dados) >= 3 else dados

    # Calcula as diferenças de temperatura e umidade entre os dias passados
    diffs_temp = []
    diffs_umi = []
    for i in range(1, len(ultimos_dias)):
        diffs_temp.append(ultimos_dias[i]["temp"] - ultimos_dias[i - 1]["temp"])
        diffs_umi.append(
            ultimos_dias[i]["umidade"] - ultimos_dias[i - 1]["umidade"]
        )

    # Tendência média
    tendencia_temp = sum(diffs_temp) / len(diffs_temp)
    tendencia_umi = sum(diffs_umi) / len(diffs_umi)

    # Projeção baseada no último dia real inserido
    temp_prevista = ultimos_dias[-1]["temp"] + tendencia_temp
    umi_prevista = max(0, min(100, ultimos_dias[-1]["umidade"] + tendencia_umi))

    # Lógica de probabilidade de chuva baseada na variação da umidade e temp
    if umi_prevista > 75 and tendencia_temp < 0:
        chuva_prevista = "Alta probabilidade de chuva / Tempestade"
    elif umi_prevista > 60:
        chuva_prevista = "Possibilidade de chuvas isoladas"
    else:
        chuva_prevista = "Tempo limpo / Sem previsão de chuva"

    return {
        "temp": round(temp_prevista, 1),
        "umidade": round(umi_prevista, 1),
        "chuva": chuva_prevista,
    }


def detectar_riscos(dados):
    """Varre o histórico para alertar sobre anomalias críticas ou mudanças bruscas."""
    alertas = []
    if not dados:
        return alertas

    # Analisa o último dia digitado
    ultimo = dados[-1]

    if ultimo["temp"] >= 35.0:
        alertas.append(
            f"⚠️ ONDA DE CALOR: Temperatura crítica detectada em {ultimo['data']} ({ultimo['temp']}°C)."
        )

    if ultimo["umidade"] <= 30:
        alertas.append(
            f"BAIXA UMIDADE: Risco à saúde/queimadas em {ultimo['data']} ({ultimo['umidade']}%)."
        )

    if ultimo["chuva"] >= 40.0:
        alertas.append(
            f"TEMPESTADE: Alto volume de precipitação em {ultimo['data']} ({ultimo['chuva']}mm)."
        )

    # Analisa mudanças bruscas de um dia para o outro
    if len(dados) >= 2:
        penultimo = dados[-2]
        queda_temp = penultimo["temp"] - ultimo["temp"]
        if queda_temp >= 5.0:
            alertas.append(
                f"⚡ CHOQUE TÉRMICO: Queda abrupta de temperatura entre {penultimo['data']} e {ultimo['data']} (-{queda_temp}°C)."
            )

    return alertas


def exibir_painel():
    """Imprime os resultados analíticos na tela."""
    stats = analisar_historico(dados_climaticos)

    if not stats:
        print("Nenhum dado foi inserido para análise.")
        return

    print("=" * 55)
    print("                PAINEL DE ANÁLISE FINAL                ")
    print("=" * 55)

    # 1. Resumo Estatístico
    print("\n ESTATÍSTICAS DO PERÍODO:")
    print(f"  • Dias Analisados:    {len(dados_climaticos)}")
    print(f"  • Temp. Média:        {stats['media_temp']:.1f}°C")
    print(f"  • Limites Térmicos:   {stats['temp_min']}°C a {stats['temp_max']}°C")
    print(f"  • Umidade Média:      {stats['media_umi']:.1f}%")
    print(f"  • Chuva Acumulada:    {stats['total_chuva']:.1f} mm")
    print("-" * 55)

    # 2. Detecção de Riscos
    print(" PADRÕES DE RISCO DETECTADOS:")
    alertas = detectar_riscos(dados_climaticos)
    if alertas:
        for alerta in alertas:
            print(f"  {alerta}")
    else:
        print("  Nenhum padrão de risco extremo encontrado.")
    print("-" * 55)

    # 3. Previsão
    print("PREVISÃO PARA O DIA SEGUINTE:")
    previsao = prever_proximo_dia(dados_climaticos)
    if isinstance(previsao, dict):
        print(f"  • Temp. Estimada:     {previsao['temp']}°C")
        print(f"  • Umidade Estimada:   {previsao['umidade']}%")
        print(f"  • Tendência do Tempo: {previsao['chuva']}")
    else:
        print(f"  {previsao}")
    print("=" * 55)


# --- Execução Principal ---
if __name__ == "__main__":
    coletar_dados_input()
    exibir_painel()