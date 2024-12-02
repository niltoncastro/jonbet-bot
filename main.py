import os
import time
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import requests
import json

# Variável global para armazenar o código da próxima partida
proxima_partida = None


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
            if "2359744937144225792" in link['href'] and "prematch" in link['href'].lower():
                links.append(link['href'])
                download_and_save_json(link['href'])  # Baixar e salvar o JSON
        return links
    except Exception as e:
        display_message(f"Erro ao processar o HTML: {str(e)}")
        return []


def salvar_dados_proxima_partida(json_content):
    """Salva os dados da próxima partida se atender às condições."""
    global proxima_partida

    events = json_content.get("events", {})
    for key, value in events.items():
        if isinstance(value, dict):
            match_status = value.get("state", {}).get("match_status")
            tournament = value.get("desc", {}).get("tournament")
            competitors = value.get("desc", {}).get("competitors")
            codigo = key

            # Condição: "match_status": 0, torneio correto e código da partida é diferente
            if (
                match_status == 0 and
                tournament == "2361937986599399439" and  # Filtra apenas o torneio correto
                (not proxima_partida or codigo != proxima_partida)
            ):
                proxima_partida = codigo  # Atualiza o código da próxima partida
                if competitors and len(competitors) == 2:
                    time1 = competitors[0].get("name", "Time1 desconhecido")
                    time2 = competitors[1].get("name", "Time2 desconhecido")
                    display_message(f"Partida agendada. Código: {codigo} - {time1} x {time2}")
                    return {codigo: value}  # Retorna apenas o objeto do torneio
                else:
                    display_message(f"Dados inconsistentes para a próxima partida no código: {codigo}")
                break  # Para garantir que apenas o primeiro objeto seja considerado
    return None


def download_and_save_json(url):
    """Faz download do JSON e salva os dados relevantes."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            prefix = "prematch_"
            file_name = prefix + url.split("/")[-1] + ".json"
            file_path = os.path.join("C:/Users/junio/Desktop/temp/log-jonbet", file_name)

            json_content = response.json()
            events = json_content.get("events", {})

            # Filtra os dados do torneio e salva apenas se houver alteração ou na primeira execução
            if events:
                salvar_dados = None
                for key, value in events.items():
                    if (
                        isinstance(value, dict) and
                        value.get("state", {}).get("match_status") == 0 and
                        value.get("desc", {}).get("tournament") == "2361937986599399439"
                    ):
                        salvar_dados = {key: value}  # Salva apenas o objeto relevante
                        break  # Considera apenas o primeiro objeto

                if salvar_dados and (not proxima_partida or key != proxima_partida):
                    with open(file_path, "w", encoding="utf-8") as f:
                        json.dump(salvar_dados, f, ensure_ascii=False, indent=4)
                    # display_message(f"Arquivo prematch salvo com sucesso: {file_path}")

                    # Atualiza a próxima partida
                    salvar_dados_proxima_partida({"events": salvar_dados})

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
