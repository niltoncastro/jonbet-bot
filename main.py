from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

# Configuração do GeckoDriver (Firefox)
webdriver_service = Service('C:/Users/junio/Desktop/workspace/python/jonbet-develop/venv/geckodriver.exe')

# Caminho para o perfil do Firefox existente
profile_path = "C:/Users/junio/AppData/Roaming/Mozilla/Firefox/Profiles/3o86k8j1.default-release"

# Configurações do Firefox
firefox_options = Options()
firefox_options.binary_location = "C:/Program Files/Mozilla Firefox/firefox.exe"  # Caminho para o executável do Firefox
firefox_options.add_argument(f"--profile={profile_path}")  # Usar o perfil diretamente

# Inicializar o Firefox com o perfil existente
driver = webdriver.Firefox(service=webdriver_service, options=firefox_options)

try:
    driver.get("https://jonbet.com/pt/sports?bt-path=%2Ffifa%2Fvenezuela%2Fliga-futve-2361937986599399439")
    print("Firefox iniciado com o perfil existente!")
except Exception as e:
    print(f"Ocorreu um erro: {e}")
