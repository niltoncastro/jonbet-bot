import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

from display_message import display_message
from get_links_from_html import get_links_from_html


def access_url(url):
    """Função principal para automação do navegador."""
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
