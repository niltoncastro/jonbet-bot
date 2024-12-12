import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from display_message import display_message
from get_links_from_html import get_links_from_html
from log_writer import log_writer


def iniciar_driver():
    """Inicializa o driver do Firefox."""
    webdriver_service = Service('C:/Users/junio/Desktop/workspace/python/jonbet-develop/venv/geckodriver.exe')
    profile_path = "C:/Users/junio/AppData/Roaming/Mozilla/Firefox/Profiles/3o86k8j1.default-release"
    firefox_options = Options()
    firefox_options.binary_location = "C:/Program Files/Mozilla Firefox/firefox.exe"
    firefox_options.add_argument(f"--profile={profile_path}")
    firefox_options.add_argument("--headless")  # Executar em modo headless para reduzir uso de memória
    driver = webdriver.Firefox(service=webdriver_service, options=firefox_options)
    return driver


def browser_automation(url):
    """Função principal para automação do navegador."""
    reiniciar_intervalo = 100  # Número de iterações antes de reiniciar o 'driver'
    iteracao = 0

    driver = iniciar_driver()

    while True:
        try:
            driver.get(url)
        except Exception as e:
            message = f"-- Página {url} com erro de acesso: {str(e)}"
            display_message(message)
            log_writer(message)
            time.sleep(5)  # Aguarda antes de tentar novamente
            continue

        time.sleep(10)  # Aguarda carregamento da página

        try:
            html_source = driver.page_source

            # Processa liga Venezuela
            codigo_liga = "2361937986599399439"
            get_links_from_html(codigo_liga, html_source)

        except Exception as e:
            message = f"Erro durante a execução principal: {str(e)}"
            display_message(message)
            log_writer(message)

        iteracao += 1
        if iteracao >= reiniciar_intervalo:
            # Reinicia o driver periodicamente
            driver.quit()
            driver = iniciar_driver()
            iteracao = 0

    driver.quit()
