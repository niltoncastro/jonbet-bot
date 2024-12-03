import requests

from display_message import display_message
from process_steps_game import process_steps_game



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
