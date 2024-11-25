from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time
import traceback

# Configuração do GeckoDriver (Firefox)
webdriver_service = Service('C:/Users/junio/Desktop/workspace/python/jonbet-develop/venv/geckodriver.exe')

# Caminho para o perfil do Firefox existente
profile_path = "C:/Users/junio/AppData/Roaming/Mozilla/Firefox/Profiles/3o86k8j1.default-release"

# Configurações do Firefox
firefox_options = Options()
firefox_options.binary_location = "C:/Program Files/Mozilla Firefox/firefox.exe"  # Caminho para o executável do Firefox
firefox_options.add_argument(f"--profile={profile_path}")  # Usar o perfil diretamente

# Inicializar o Firefox com o perfil existente
try:
    driver = webdriver.Firefox(service=webdriver_service, options=firefox_options)
    print("Firefox iniciado com sucesso!")

    while True:  # Loop infinito para manter a aplicação em execução
        try:
            # Acessar a página
            print("Acessando a página...")
            driver.get("https://jonbet.com/pt/sports?bt-path=%2Ffifa%2Fvenezuela%2Fliga-futve-2361937986599399439")
            print("Página acessada com sucesso!")

            # Esperar 10 segundos antes de acessar novamente
            time.sleep(10)
        except Exception as e:
            print("Erro ao acessar a página:")
            traceback.print_exc()
            # Continuar o loop mesmo em caso de erro
            time.sleep(10)

except Exception as e:
    print("Ocorreu um erro ao iniciar o Firefox:")
    traceback.print_exc()

finally:
    # Garantir que o navegador será fechado ao encerrar o script
    try:
        driver.quit()
        print("Navegador fechado.")
    except NameError:
        print("Driver não foi inicializado.")
