def get_team_year_id(team: int, year: int):
    return int(str(year) + str(team))


def get_team_event_key(team: int, event: str) -> str:
    return str(team) + "-" + event


def get_team_match_key(team: int, match: str) -> str:
    return str(team) + "-" + match
