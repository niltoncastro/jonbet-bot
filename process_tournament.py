import requests

from display_message import display_message
from log_writer import log_writer
from process_steps_game import process_steps_game


def process_tournament(url, codigo_liga):
    # print("process_tournament")

    """Faz download do JSON 'live' e processa os estados do jogo."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            json_content = response.json()
            events = json_content.get("events", {})

            for key, value in events.items():
                if value.get("desc", {}).get("tournament") == codigo_liga:
                    process_steps_game(value, key, codigo_liga)
        else:
            message = f"Erro ao acessar {url}, status code: {response.status_code}"
            display_message(message)
            log_writer(message)
    except Exception as e:
        display_message(f"Erro ao tentar baixar o conteúdo de {url}: {str(e)}")
