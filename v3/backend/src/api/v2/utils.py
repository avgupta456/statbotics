def format_team(team: str) -> int:
    if not team[-1].isdigit():
        team = team[:-1] + "000" + str(ord(team[-1]) - ord("A")).rjust(2, "0")
    return int(team)


def inv_format_team(team: int) -> str:
    if team > 100000:
        return str(round(team / 100000, 0)) + chr(65 + (team % 100000))
    return str(team)


def format_type(type: str) -> int:
    if type == "invalid":
        return -1
    elif type == "regional":
        return 0
    elif type == "district":
        return 1
    elif type == "district_cmp":
        return 2
    elif type == "champs_div":
        return 3
    elif type == "einstein":
        return 4
    elif type == "offseason":
        return 99
    elif type == "preseason":
        return 100

    return 0
