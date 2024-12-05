from datetime import datetime

from db_utils import insert_resultado
from display_message import display_message
from mappings import format_team_name, state_description
from mappings import league_name

# Variáveis globais
codigo_partida_agendada = None
codigo_partida_atual = None
time_casa = None
time_casa_agendado = None
time_visitante = None
time_visitante_agendado = None
placar_casa = "0"
placar_visitante = "0"
placar_anterior = (0, 0)
sigla_estado_partida = None
tempo_partida = None
descricao_estado_partida = None
data_partida = None
data_criacao = None
placar_1T = None
placar_2T = None
flg_final = None
tipo_resultado = None
descricao_resultado = None
resultado_partida = None
flg_virada = None
flg_atualiza_banco = "N"


def process_steps_game(evento, codigo_partida, codigo_liga):
    """Processa os estados do jogo a partir do arquivo 'live'."""
    global codigo_partida_agendada, codigo_partida_atual, time_casa, time_casa_agendado, time_visitante, time_visitante_agendado, placar_casa, \
        placar_visitante, placar_anterior, sigla_estado_partida, tempo_partida, descricao_estado_partida, data_partida, data_criacao, placar_1T, \
        placar_2T, flg_final, tipo_resultado, descricao_resultado, resultado_partida, flg_virada, flg_atualiza_banco

    data_partida = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    data_criacao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    match_status = evento.get("state", {}).get("match_status")
    nome_liga = league_name(codigo_liga)
    times = evento.get("desc", {}).get("competitors")
    tempo_partida = evento.get('state', {}).get('clock', {}).get('match_time', '00:00')

    # 1_Aguardando início da partida [AI]
    if match_status == 20 and (sigla_estado_partida == "PF" or not sigla_estado_partida):
        sigla_estado_partida = "AI"
        descricao_estado_partida = state_description(sigla_estado_partida)
        codigo_partida_atual = codigo_partida
        time_casa = format_team_name(times[0].get("name", "time_casa"))
        time_visitante = format_team_name(times[1].get("name", "Time visitante"))
        flg_atualiza_banco = "S"

        display_message(
            f"Aguardando início da partida. Código: {codigo_partida_atual} - {time_casa} x {time_visitante}")

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

                display_message(
                    f"Partida agendada. Código: {codigo_partida_agendada} - {time_casa_agendado} x {time_visitante_agendado}")

    # 3_Início do primeiro tempo [1T]
    if match_status == 6 and sigla_estado_partida == "PA":
        sigla_estado_partida = "1T"
        descricao_estado_partida = state_description(sigla_estado_partida)
        placar_casa = int(evento.get("score", {}).get("home_score", 0))
        placar_visitante = int(evento.get("score", {}).get("away_score", 0))
        placar_1T = f"{placar_casa}x{placar_visitante}"
        flg_atualiza_banco = "S"

        display_message(
            f"Iniciou o primeiro tempo da partida. "f"{time_casa} {placar_casa} x {placar_visitante} {time_visitante}")

    # 4_Início do segundo tempo (2T)
    if match_status == 7 and sigla_estado_partida == "1T":
        sigla_estado_partida = "2T"
        descricao_estado_partida = state_description(sigla_estado_partida)
        flg_atualiza_banco = "S"

        display_message(
            f"Iniciou o segundo tempo da partida. "f"{time_casa} {placar_casa} x {placar_visitante} {time_visitante}")

    # 5_Atualização da partida [1T ou 2T]
    if match_status != 100 and sigla_estado_partida in ["1T", "2T"]:
        placar_casa_atual = int(evento.get("score", {}).get("home_score", placar_casa))
        placar_visitante_atual = int(evento.get("score", {}).get("away_score", placar_visitante))

        if (placar_casa_atual, placar_visitante_atual) != (placar_casa, placar_visitante):
            placar_anterior = (placar_casa_atual, placar_visitante_atual)
            flg_atualiza_banco = "S"
            if placar_casa_atual != placar_casa:
                placar_casa = placar_casa_atual
                descricao_estado_partida = f"GOL do {time_casa}"
                display_message(
                    f"GOL do {time_casa} - tempo: {tempo_partida}")
            if placar_visitante_atual != placar_visitante:
                placar_visitante = placar_visitante_atual
                descricao_estado_partida = f"GOL do {time_casa}"
                display_message(
                    f"GOL do {time_visitante} - tempo: {tempo_partida}")

            display_message(f"Placar: {time_casa} {placar_casa} x {placar_visitante} {time_visitante}")

    # 6_Finalização do jogo [PF]
    if match_status == 100 and sigla_estado_partida == "2T":
        sigla_estado_partida = "PF"
        descricao_estado_partida = state_description(sigla_estado_partida)
        flg_final = "S"
        flg_virada = "N"
        period_scores = evento.get("score", {}).get("period_scores", [])
        primeiro_tempo = next((p for p in period_scores if p.get("match_status_code") == 6), {})
        home_1T = int(primeiro_tempo.get("home_score", 0))
        away_1T = int(primeiro_tempo.get("away_score", 0))
        flg_atualiza_banco = "S"

        if (home_1T < away_1T and placar_casa > placar_visitante) or (
                away_1T < home_1T and placar_visitante > placar_casa):
            flg_virada = "S"
            display_message(f"{time_casa if placar_casa > placar_visitante else time_visitante} venceu de virada!")

        if placar_casa > placar_visitante:
            tipo_resultado = 'CASA'
            resultado_partida = time_casa

        if placar_casa > placar_visitante:
            tipo_resultado = 'VISITANTE'
            resultado_partida = time_visitante

        if placar_casa == placar_visitante:
            tipo_resultado = 'EMPATE'
            resultado_partida = "EMPATE"

        display_message(f"Fim da Partida. Código: {codigo_partida_atual} - "
                        f"Placar final: {time_casa} {placar_casa} x {placar_visitante} {time_visitante}. Virada: {flg_virada}")
        print("---------------------------------------------------------------------------------------------")

    # ATUALIZACAO DO BANCO DE DADOS
    if flg_atualiza_banco == "S":
        insert_resultado(codigo_partida, codigo_liga, nome_liga, time_casa, placar_casa, time_visitante,
                         placar_visitante, tempo_partida, placar_1T, placar_2T, sigla_estado_partida,
                         descricao_estado_partida, flg_final, tipo_resultado, descricao_resultado,
                         resultado_partida, flg_virada, data_partida, data_criacao)
