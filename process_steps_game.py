from display_message import display_message
from mappings import format_team_name

# Variáveis globais
codigo_partida_agendada = None
codigo_partida_atual = None
home_team = None
away_team = None
home_score = 0
away_score = 0
placar_anterior = (0, 0)
estado_partida = None


def process_steps_game(event, event_id):
    """Processa os estados do jogo a partir do arquivo 'live'."""
    global codigo_partida_agendada, estado_partida, codigo_partida_atual, home_team, away_team, home_score, away_score, placar_anterior

    match_status = event.get("state", {}).get("match_status")
    competitors = event.get("desc", {}).get("competitors")

    # 1 - Aguardando início da partida [AI]
    if match_status == 20 and (estado_partida == "PF" or not estado_partida):
        estado_partida = "AI"
        codigo_partida_atual = event_id
        if competitors and len(competitors) == 2:
            home_team = format_team_name(competitors[0].get("name", "Time casa"))
            away_team = format_team_name(competitors[1].get("name", "Time visitante"))
            display_message(f"Aguardando início da partida. Código: {codigo_partida_atual} - {home_team} x {away_team}")

    # 2 - Dados da partida agendada [AG]
    if match_status == 0 and estado_partida == "AI":
        if event_id != codigo_partida_atual:
            if not codigo_partida_agendada or event_id != codigo_partida_agendada:
                estado_partida = "AG"
                codigo_partida_agendada = event_id
                if competitors and len(competitors) == 2:
                    time1 = competitors[0].get("name", "Time1 desconhecido")
                    time2 = competitors[1].get("name", "Time2 desconhecido")
                    display_message(f"Partida agendada. Código: {codigo_partida_agendada} - {time1} x {time2}")

    # 3 - Início do primeiro tempo [1T]
    if match_status == 6 and estado_partida == "AG":
        estado_partida = "1T"
        home_score = int(event.get("score", {}).get("home_score", 0))
        away_score = int(event.get("score", {}).get("away_score", 0))
        placar_anterior = (home_score, away_score)
        display_message(f"Iniciou o primeiro tempo da partida. "f"{home_team} {home_score} x {away_score} {away_team}")

    # 4 - Início do segundo tempo (2T)
    if match_status == 7 and estado_partida == "1T":
        estado_partida = "2T"
        display_message(f"Iniciou o segundo tempo da partida. "f"{home_team} {home_score} x {away_score} {away_team}")

    # 5 - Atualização do jogo [1T ou 2T]
    if match_status != 100 and estado_partida in ["1T", "2T"]:
        novo_home_score = int(event.get("score", {}).get("home_score", home_score))
        novo_away_score = int(event.get("score", {}).get("away_score", away_score))

        if (novo_home_score, novo_away_score) != (home_score, away_score):
            placar_anterior = (novo_home_score, novo_away_score)

            if novo_home_score != home_score:
                home_score = novo_home_score
                display_message(
                    f"GOL do {home_team} - tempo: {event.get('state', {}).get('clock', {}).get('match_time', '00:00')}")
            if novo_away_score != away_score:
                away_score = novo_away_score
                display_message(
                    f"GOL do {away_team} - tempo: {event.get('state', {}).get('clock', {}).get('match_time', '00:00')}")

            display_message(f"Placar: {home_team} {home_score} x {away_score} {away_team}")

    # 6 - Finalização do jogo [PF]
    if match_status == 100 and estado_partida == "2T":
        estado_partida = "PF"
        virada = "N"
        period_scores = event.get("score", {}).get("period_scores", [])
        primeiro_tempo = next((p for p in period_scores if p.get("match_status_code") == 6), {})
        home_1T = int(primeiro_tempo.get("home_score", 0))
        away_1T = int(primeiro_tempo.get("away_score", 0))

        if (home_1T < away_1T and home_score > away_score) or (away_1T < home_1T and away_score > home_score):
            virada = "S"
            display_message(f"{home_team if home_score > away_score else away_team} venceu de virada!")

        display_message(f"Fim da Partida. Código: {codigo_partida_atual} - "
                        f"Placar final: {home_team} {home_score} x {away_score} {away_team}. Virada: {virada}")
        print("---------------------------------------------------------------------------------------------")
