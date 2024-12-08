def format_team_name(parameter):
    mapping = {
        "Dep. Táchira": "Tachira",
        "Dep. La Guaira": "Guaira",
        "Caracas F.C.": "Caracas"
    }
    return mapping.get(parameter, parameter)


def league_name(parameter):
    mapping = {
        "2361937986599399439": "Venezuela"
    }

    return mapping.get(parameter, parameter)


def table_name(parameter):
    mapping = {
        "2361937986599399439": "venezuela_fifa_resultados"
    }

    return mapping.get(parameter, parameter)


def paths(parameter):
    mapping = {
        "file_server_local": "C:\\Users\\junio\\Desktop\\workspace\\python\\jonbet-bot\\files\\",
        "file_server_gdrive": "G:/Meu Drive/workspace/jonbet/"
    }

    return mapping.get(parameter, parameter)


def state_description(parameter):
    mapping = {
        "AI": "Aguardando Inicio",
        "1T": "Primeiro Tempo",
        "2T": "Segundo Tempo",
        "PF": "Partida Finalizada"
    }
    return mapping.get(parameter, parameter)
