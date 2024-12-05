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


def state_description(parameter):
    mapping = {
        "AI": "Aguardando Inicio",
        "1T": "Primeiro Tempo",
        "2T": "Segundo Tempo",
        "PF": "Partida Finalizada"
    }
    return mapping.get(parameter, parameter)
