
# 1. Base de Dados de Exemplo (Simulando leituras diárias: Data, Temp °C, Umidade %, Chuva mm)
dados_climaticos = [
    {"data": "2026-05-25", "temp": 22.5, "umidade": 65, "chuva": 0.0},
    {"data": "2026-05-26", "temp": 24.0, "umidade": 60, "chuva": 0.0},
    {"data": "2026-05-27", "temp": 26.8, "umidade": 55, "chuva": 2.5},
    {"data": "2026-05-28", "temp": 29.5, "umidade": 48, "chuva": 0.0},
    {"data": "2026-05-29", "temp": 31.0, "umidade": 40, "chuva": 0.0},
    {"data": "2026-05-30", "temp": 33.5, "umidade": 35, "chuva": 0.0},
    {"data": "2026-05-31", "temp": 35.0, "umidade": 30, "chuva": 0.0},
    {"data": "2026-06-01", "temp": 28.0, "umidade": 85,
        "chuva": 45.0},  # Queda abrupta e muita chuva
]


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
    """Gera uma previsão simples baseada na tendência dos últimos 3 dias."""
    if len(dados) < 3:
        return "Dados insuficientes para prever estatisticamente."

    # Pegamos os 3 últimos dias para ver a tendência
    ultimos_dias = dados[-3:]

    # Tendência de Temperatura (Diferença média dia a dia)
    diff_temp_1 = ultimos_dias[1]["temp"] - ultimos_dias[0]["temp"]
    diff_temp_2 = ultimos_dias[2]["temp"] - ultimos_dias[1]["temp"]
    tendencia_temp = (diff_temp_1 + diff_temp_2) / 2

    # Tendência de Umidade
    diff_umi_1 = ultimos_dias[1]["umidade"] - ultimos_dias[0]["umidade"]
    diff_umi_2 = ultimos_dias[2]["umidade"] - ultimos_dias[1]["umidade"]
    tendencia_umi = (diff_umi_1 + diff_umi_2) / 2

    # Projeção para o dia seguinte
    temp_prevista = ultimos_dias[2]["temp"] + tendencia_temp
    umi_prevista = max(
        0, min(100, ultimos_dias[2]["umidade"] + tendencia_umi)
    )  # Mantém entre 0 e 100%

    # Lógica simples de probabilidade de chuva
    if umi_prevista > 75 and tendencia_temp < 0:
        chuva_prevista = "Alta probabilidade de chuva"
    elif umi_prevista > 60:
        chuva_prevista = "Possibilidade de chuva isolada"
    else:
        chuva_prevista = "Tempo seco / Sem chuva"

    return {
        "temp": round(temp_prevista, 1),
        "umidade": round(umi_prevista, 1),
        "chuva": chuva_prevista,
    }


def detectar_riscos(dados):
    """Varre os dados e as tendências para alertar sobre anomalias perigosas."""
    alertas = []
    if not dados:
        return alertas

    ultimo_registro = dados[-1]

    # 1. Risco de Ondas de Calor (Ex: Temperatura > 34°C)
    if ultimo_registro["temp"] >= 35.0:
        alertas.append(
            f"⚠️ ALERTA DE ONDA DE CALOR: Temperatura extrema registrada ({ultimo_registro['temp']}°C)."
        )

    # 2. Risco de Baixa Umidade (Prejudicial à saúde)
    if ultimo_registro["umidade"] <= 30:
        alertas.append(
            f"⚠️ ALERTA DE BAIXA UMIDADE: Ar muito seco ({ultimo_registro['umidade']}%). Hidrate-se!"
        )

    # 3. Risco de Tempestade / Inundação
    if ultimo_registro["chuva"] >= 40.0:
        alertas.append(
            f"🚨 ALERTA DE TEMPESTADE: Volume de chuva crítico detectado ({ultimo_registro['chuva']}mm)."
        )

    # 4. Análise de Mudança Abrupta (Choque térmico / Frente fria)
    if len(dados) >= 2:
        penultimo = dados[-2]
        queda_temp = penultimo["temp"] - ultimo_registro["temp"]
        if queda_temp >= 5.0:
            alertas.append(
                f"⚡ MUDANÇA BRUSCA: Queda rápida de temperatura detectada (-{queda_temp}°C em 24h)."
            )

    return alertas


# --- Interface do Terminal ---
def exibir_painel():
    print("=" * 55)
    print("         SISTEMA DE ANÁLISE CLIMÁTICA NATIVO         ")
    print("=" * 55)

    # Executa as análises
    stats = analisar_historico(dados_climaticos)
    previsao = prever_proximo_dia(dados_climaticos)
    alertas = detectar_riscos(dados_climaticos)

    # Exibe Resumo
    print("\n📊 RESUMO DO PERÍODO HISTÓRICO:")
    print(f"  • Temperatura Média: {stats['media_temp']:.1f}°C")
    print(
        f"  • Amplitude Térmica: {stats['temp_min']}°C a {stats['temp_max']}°C")
    print(f"  • Umidade Média:     {stats['media_umi']:.1f}%")
    print(f"  • Acumulado de Chuva: {stats['total_chuva']:.1f} mm")

    print("-" * 55)

    # Exibe Alertas de Risco
    print("🚨 DETECÇÃO DE PADRÕES DE RISCO:")
    if alertas:
        for alerta in alertas:
            print(f"  {alerta}")
    else:
        print("  ✅ Nenhum padrão de risco crítico detectado no momento.")

    print("-" * 55)

    # Exibe Previsão
    print("🔮 PREVISÃO ESTATÍSTICA PARA AMANHÃ:")
    if isinstance(previsao, dict):
        print(f"  • Temperatura Estimada: {previsao['temp']}°C")
        print(f"  • Umidade Estimada:     {previsao['umidade']}%")
        print(f"  • Condição:             {previsao['chuva']}")
    else:
        print(previsao)
    print("=" * 55)


if __name__ == "__main__":
    exibir_painel()
