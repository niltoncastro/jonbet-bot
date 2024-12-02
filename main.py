import os
import time
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import requests
import json

# Variáveis globais
proxima_partida = None
estado_partida = None
codigo_partida = None
home_team = None
away_team = None
home_score = 0
away_score = 0
placar_anterior = (0, 0)


def display_message(message):
    """Exibe mensagens formatadas com a data e hora."""
    current_time = datetime.now().strftime('%Y%m%d%H%M%S')
    formatted_message = f"{current_time} - {message}"
    print(formatted_message)


def get_links_from_html(html_source):
    """Extrai os links da página HTML."""
    try:
        soup = BeautifulSoup(html_source, 'html.parser')
        links = []
        for link in soup.find_all('link', href=True):
            if "2359744937144225792" in link['href'].lower():
                links.append(link['href'])
                process_tournament(link['href'])
        return links
    except Exception as e:
        display_message(f"Erro ao processar o HTML: {str(e)}")
        return []


def process_steps_game(event, event_id):
    """Processa os estados do jogo a partir do arquivo 'live'."""
    global proxima_partida, estado_partida, codigo_partida, home_team, away_team, home_score, away_score, placar_anterior

    # Primeira etapa: salvar dados da próxima partida
    match_status = event.get("state", {}).get("match_status")
    tournament = event.get("desc", {}).get("tournament")
    competitors = event.get("desc", {}).get("competitors")

    if match_status == 0 and tournament == "2361937986599399439":
        if not proxima_partida or event_id != proxima_partida:
            proxima_partida = event_id
            if competitors and len(competitors) == 2:
                time1 = competitors[0].get("name", "Time1 desconhecido")
                time2 = competitors[1].get("name", "Time2 desconhecido")
                display_message(f"Partida agendada. Código: {event_id} - {time1} x {time2}")

    # Aguardando início da partida (AI)
    if match_status == 20 and estado_partida != "AI":
        estado_partida = "AI"
        codigo_partida = event_id
        if competitors and len(competitors) == 2:
            home_team = competitors[0].get("name", "Time casa")
            away_team = competitors[1].get("name", "Time visitante")
            display_message(f"Aguardando início da partida. Código: {codigo_partida} - {home_team} x {away_team}")

    # Início do primeiro tempo (1T)
    elif match_status == 6 and estado_partida == "AI":
        estado_partida = "1T"
        home_score = int(event.get("score", {}).get("home_score", 0))
        away_score = int(event.get("score", {}).get("away_score", 0))
        placar_anterior = (home_score, away_score)
        display_message(f"Iniciou o primeiro tempo da partida. Código: {codigo_partida} - "
                        f"{home_team} {home_score} x {away_score} {away_team}")

    # Início do segundo tempo (2T)
    elif match_status == 7 and estado_partida == "1T":
        estado_partida = "2T"
        display_message(f"Iniciou o segundo tempo da partida. Código: {codigo_partida} - "
                        f"{home_team} {home_score} x {away_score} {away_team}")

    # Atualização do jogo (1T ou 2T)
    elif match_status != 100 and estado_partida in ["1T", "2T"]:
        novo_home_score = int(event.get("score", {}).get("home_score", home_score))
        novo_away_score = int(event.get("score", {}).get("away_score", away_score))

        if (novo_home_score, novo_away_score) != placar_anterior:
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

    # Finalização do jogo (PF)
    elif match_status == 100 and estado_partida == "2T":
        estado_partida = "PF"
        placar_final = (home_score, away_score)
        virada = "N"

        period_scores = event.get("score", {}).get("period_scores", [])
        primeiro_tempo = next((p for p in period_scores if p.get("match_status_code") == 6), {})
        home_1T = int(primeiro_tempo.get("home_score", 0))
        away_1T = int(primeiro_tempo.get("away_score", 0))

        if (home_1T < away_1T and home_score > away_score) or (away_1T < home_1T and away_score > home_score):
            virada = "S"
            display_message(f"{home_team if home_score > away_score else away_team} venceu de virada!")

        display_message(f"Fim da Partida. Código: {codigo_partida} - "
                        f"Placar final: {home_team} {home_score} x {away_score} {away_team}. Virada: {virada}")
        print("---------------------------------------------------------------------------------------------")


def process_tournament(url):
    """Faz download do JSON 'live' e processa os estados do jogo."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            json_content = response.json()
            events = json_content.get("events", {})

            for key, value in events.items():
                if value.get("desc", {}).get("tournament") == "2361937986599399439":
                    process_steps_game(value, key)
        else:
            display_message(f"Erro ao acessar {url}, status code: {response.status_code}")
    except Exception as e:
        display_message(f"Erro ao tentar baixar o conteúdo de {url}: {str(e)}")


def main():
    """Função principal para automação do navegador."""
    url = "https://jonbet.com/pt/sports?bt-path=%2Ffifa%2Fvenezuela%2Fliga-futve-2361937986599399439"

    webdriver_service = Service('C:/Users/junio/Desktop/workspace/python/jonbet-develop/venv/geckodriver.exe')
    profile_path = "C:/Users/junio/AppData/Roaming/Mozilla/Firefox/Profiles/3o86k8j1.default-release"

    firefox_options = Options()
    firefox_options.binary_location = "C:/Program Files/Mozilla Firefox/firefox.exe"
    firefox_options.add_argument(f"--profile={profile_path}")

    driver = webdriver.Firefox(service=webdriver_service, options=firefox_options)

    while True:
        try:
            driver.get(url)
        except Exception as e:
            display_message("-- Página " + url + " com erro de acesso")
            continue

        time.sleep(10)

        try:
            html_source = driver.page_source
            get_links_from_html(html_source)
        except Exception as e:
            display_message(f"Erro durante a execução principal: {str(e)}")

    driver.quit()


if __name__ == "__main__":
    main()
