def format_team_name(var):
    name_mapping = {
        "Dep. Táchira": "Tachira",
        "Dep. La Guaira": "Guaira",
        "Caracas F.C": "Caracas",
    }
    return name_mapping.get(var, var)


def description_league(var):
    description_mapping = {
        "Dep. Táchira": "Tachira",
        "Dep. La Guaira": "Guaira",
        "Caracas F.C": "Caracas",
    }
    return description_mapping.get(var, var)

