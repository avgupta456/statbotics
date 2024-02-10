def get_team_year_id(team: int, year: int):
    return int(str(year) + str(team))


def get_team_event_key(team: int, event: str) -> str:
    return str(team) + "-" + event


def get_team_match_key(team: int, match: str) -> str:
    return str(team) + "-" + match


def get_match_name(key: str) -> str:
    if "_" in key:
        key = key.split("_")[1]

    if "qm" in key:
        return "Qual " + key.split("qm")[1]
    elif "qf" in key:
        set_num = key.split("qf")[1].split("m")[0]
        match_num = key.split("qf")[1].split("m")[1]
        return "Quarters " + set_num + " Match " + match_num
    elif "sf" in key:
        set_num = key.split("sf")[1].split("m")[0]
        match_num = key.split("sf")[1].split("m")[1]
        return "Semis " + set_num + " Match " + match_num
    elif "f" in key:
        return "Finals Match " + key.split("f")[1].split("m")[1]

    raise Exception("Invalid match key")


def get_match_number(key: str) -> int:
    if "_" in key:
        key = key.split("_")[1]

    if "qm" in key:
        return int(key.split("qm")[1])
    elif "qf" in key:
        set_num = key.split("qf")[1].split("m")[0]
        match_num = key.split("qf")[1].split("m")[1]
        return 100 + 10 * int(set_num) + int(match_num)
    elif "sf" in key:
        set_num = key.split("sf")[1].split("m")[0]
        match_num = key.split("sf")[1].split("m")[1]
        return 200 + 10 * int(set_num) + int(match_num)
    elif "f" in key:
        return 300 + int(key.split("f")[1].split("m")[1])

    raise Exception("Invalid match key")
