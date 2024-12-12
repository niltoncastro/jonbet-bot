from browser_automation import browser_automation


def main():
    # print("main")

    # acessar torneio da liga da venezuela
    url = "https://jonbet.com/pt/sports?bt-path=%2Ffifa%2Fvenezuela%2Fliga-futve-2361937986599399439"
    browser_automation(url)


if __name__ == "__main__":
    main()
