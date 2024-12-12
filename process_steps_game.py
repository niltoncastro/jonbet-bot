from datetime import datetime

from db_utils import insert_resultado, busca_ultimo_id
from display_message import display_message
from log_writer import log_writer
from mappings import format_team_name, state_description, table_name
from mappings import league_name
from save_resultado_planilha import save_planilha_resultado_final

# Variáveis globais
codigo_partida_agendada = None
codigo_partida_atual = None
data_criacao = None
data_partida = None
descricao_estado_partida = None
descricao_resultado = None
flg_atualiza_banco = None
flg_final = None
flg_virada = None
placar_casa_1T = None
placar_casa_2T = None
placar_visitante_1T = None
placar_visitante_2T = None
placar_atualizado_1T = None
placar_atualizado_2T = None
placar_casa = "0"
placar_visitante = "0"
placar_final = None
resultado_partida = None
sigla_estado_partida = None
tempo_partida = None
tipo_resultado = None
time_casa = None
time_casa_agendado = None
time_visitante = None
time_visitante_agendado = None
time_vencendo = None


def process_steps_game(evento, codigo_partida, codigo_liga):
    # print("process_steps_game")

    """Processa os estados do jogo a partir do arquivo 'live'."""
    global codigo_partida_agendada, codigo_partida_atual, data_criacao, data_partida, descricao_estado_partida, \
        descricao_resultado, flg_atualiza_banco, flg_final, flg_virada, placar_atualizado_1T, placar_atualizado_2T, \
        placar_casa, placar_casa_1T, placar_casa_2T, placar_final, placar_visitante, placar_visitante_1T, \
        placar_visitante_2T, resultado_partida, sigla_estado_partida, tempo_partida, time_casa, time_casa_agendado, \
        time_visitante, time_visitante_agendado, tipo_resultado, time_vencendo

    data_partida = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    data_criacao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    match_status = evento.get("state", {}).get("match_status")
    nome_liga = league_name(codigo_liga)
    times = evento.get("desc", {}).get("competitors")
    tempo_partida = evento.get('state', {}).get('clock', {}).get('match_time', '00:00')
    flg_atualiza_banco = "N"

    # 1_Aguardando início da partida [AI]
    if match_status == 20 and (sigla_estado_partida == "PF" or not sigla_estado_partida):
        # Reset de variaveis
        flg_atualiza_banco = "N"
        flg_virada = None
        flg_final = None
        placar_casa_1T = None
        placar_casa_2T = None
        placar_visitante_1T = None
        placar_visitante_2T = None
        placar_atualizado_1T = None
        placar_atualizado_2T = None
        placar_casa = "0"
        placar_visitante = "0"
        placar_final = None
        flg_virada = None
        tipo_resultado = None
        descricao_resultado = None
        resultado_partida = None

        sigla_estado_partida = "AI"

        descricao_estado_partida = state_description(sigla_estado_partida)
        codigo_partida_atual = codigo_partida
        time_casa = format_team_name(times[0].get("name", "time_casa"))
        time_visitante = format_team_name(times[1].get("name", "Time visitante"))

        message = f"Aguardando início da partida. Código: {codigo_partida_atual} - {time_casa} x {time_visitante}"
        display_message(message)
        log_writer(message)

    # 2_Dados da partida agendada [PA]
    if match_status == 0 and sigla_estado_partida == "AI":
        if codigo_partida != codigo_partida_atual:
            if not codigo_partida_agendada or codigo_partida != codigo_partida_agendada:
                sigla_estado_partida = "PA"
                descricao_estado_partida = state_description(sigla_estado_partida)
                codigo_partida_agendada = codigo_partida
                time_casa_agendado = format_team_name(times[0].get("name", "time_casa"))
                time_visitante_agendado = format_team_name(times[1].get("name", "Time visitante"))
                flg_atualiza_banco = "N"

                message = f"Partida agendada. Código: {codigo_partida_agendada} - {time_casa_agendado} x {time_visitante_agendado}"
                display_message(message)
                log_writer(message)

    # 3_Início do primeiro tempo [1T]
    if match_status == 6 and sigla_estado_partida == "PA":
        sigla_estado_partida = "1T"
        descricao_estado_partida = state_description(sigla_estado_partida)
        flg_atualiza_banco = "S"
        placar_atualizado_1T = "0x0"

        message = f"Iniciou o primeiro tempo da partida. "f"{time_casa} {placar_casa} x {placar_visitante} {time_visitante}"
        display_message(message)
        log_writer(message)

    # 4_Início do segundo tempo (2T)
    if match_status == 7 and sigla_estado_partida == "1T":
        sigla_estado_partida = "2T"
        descricao_estado_partida = state_description(sigla_estado_partida)
        placar_atualizado_2T = "0x0"
        flg_atualiza_banco = "S"

        message = f"Iniciou o segundo tempo da partida. "f"{time_casa} {placar_casa} x {placar_visitante} {time_visitante}"
        display_message(message)
        log_writer(message)

    # 5_Atualização da partida [1T ou 2T]
    if match_status != 100 and sigla_estado_partida in ["1T", "2T"]:
        placar_casa_novo = evento.get("score", {}).get("home_score", placar_casa)
        placar_visitante_novo = evento.get("score", {}).get("away_score", placar_visitante)

        # Verificacao de Gol
        if placar_casa_novo > placar_casa or placar_visitante_novo > placar_visitante:
            flg_atualiza_banco = "S"
            if placar_casa_novo > placar_casa:
                placar_casa = placar_casa_novo
                descricao_estado_partida = f"GOL do {time_casa}"

                message = f"GOL do {time_casa} - tempo: {tempo_partida}"
                display_message(message)
                log_writer(message)

            if placar_visitante_novo > placar_visitante:
                placar_visitante = placar_visitante_novo
                descricao_estado_partida = f"GOL do {time_visitante}"

                message = f"GOL do {time_visitante} - tempo: {tempo_partida}"
                display_message(message)
                log_writer(message)

            # Regra para Virada
            if placar_casa_novo == 1 and not placar_visitante_novo:
                time_vencendo = format_team_name(times[0].get("name", "time_casa"))

            if placar_visitante_novo == 1 and not placar_casa_novo:
                time_vencendo = format_team_name(times[1].get("name", "Time visitante"))

            # Atualizacao do placar do primeiro tempo
            if sigla_estado_partida == "1T":
                period_scores = evento.get("score", {}).get("period_spasscores", [])
                placar_objeto_1T = next((p for p in period_scores if p.get("match_status_code") == 6), {})
                placar_casa_1T = placar_objeto_1T.get("home_score", 0)
                placar_visitante_1T = placar_objeto_1T.get("away_score", 0)
                placar_atualizado_1T = f"{placar_casa_1T}x{placar_visitante_1T}"

            # Atualizacao do placar do primeiro tempo
            if sigla_estado_partida == "2T":
                period_scores = evento.get("score", {}).get("period_scores", [])
                placar_objeto_2T = next((p for p in period_scores if p.get("match_status_code") == 7), {})
                placar_casa_2T = placar_objeto_2T.get("home_score", 0)
                placar_visitante_2T = placar_objeto_2T.get("away_score", 0)
                placar_atualizado_2T = f"{placar_casa_2T}x{placar_visitante_2T}"

            message = f"Placar: {time_casa} {placar_casa} x {placar_visitante} {time_visitante}"
            display_message(message)
            log_writer(message)

    # 6_Finalização do jogo [PF]
    if (match_status == 100 or codigo_partida != codigo_partida_atual) and sigla_estado_partida == "2T" and match_status != 0:
        sigla_estado_partida = "PF"
        descricao_estado_partida = state_description(sigla_estado_partida)
        tempo_partida = None
        flg_final = "S"
        flg_virada = "N"
        flg_atualiza_banco = "S"

        if placar_casa > placar_visitante:
            tipo_resultado = '1'
            descricao_resultado = "Casa"
            resultado_partida = time_casa

        if placar_casa == placar_visitante:
            tipo_resultado = '2'
            descricao_resultado = "Empate"
            resultado_partida = "Empate"

        if placar_casa < placar_visitante:
            tipo_resultado = '3'
            descricao_resultado = "Visitante"
            resultado_partida = time_visitante

        if resultado_partida not in ['Empate', time_vencendo]:
            flg_virada = "S"

        placar_final = f"{placar_casa}x{placar_visitante}"

        message = f"Fim da Partida. Código: {codigo_partida_atual} - "f"Placar final: {time_casa} {placar_casa} x" \
                  f" {placar_visitante} {time_visitante}. Virada: {flg_virada}"
        display_message(message)
        log_writer(message)

        print("---------------------------------------------------------------------------------------------")
    # ATUALIZACAO DO BANCO DE DADOS
    if flg_atualiza_banco == "S":
        nome_tabela = table_name(codigo_liga)
        insert_resultado(nome_tabela, codigo_partida, codigo_liga, nome_liga, time_casa, placar_casa, time_visitante,
                         placar_visitante, tempo_partida, placar_atualizado_1T, placar_atualizado_2T,
                         sigla_estado_partida, descricao_estado_partida, placar_final, flg_final, tipo_resultado,
                         descricao_resultado, resultado_partida, flg_virada, data_partida, data_criacao)

        if sigla_estado_partida == "PF":
            save_planilha_resultado_final(nome_tabela, busca_ultimo_id(nome_tabela), time_casa, placar_casa,
                                          time_visitante, placar_visitante, codigo_partida)
