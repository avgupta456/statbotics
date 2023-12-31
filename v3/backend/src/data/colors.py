from json import dump, load
from typing import Any, Dict, List

import requests

from src.db.models import Team


def post_process(teams: List[Team], use_cache: bool = False) -> List[Team]:
    cache: Dict[str, Any] = {}
    if use_cache:
        try:
            with open("cache/colors.json", "r") as f:
                cache = load(f)
        except FileNotFoundError:
            pass

    for team in teams:
        print(team)
        if team.offseason:
            continue
        if team.team in cache:
            team.primary_color = cache[team.team]["primary"]
            team.secondary_color = cache[team.team]["secondary"]
            continue

        response = requests.get("https://frc-colors.com/api/v1/team/" + team.team)

        data = response.json()
        team.primary_color = data.get("colors", {}).get("primaryHex", None)
        team.secondary_color = data.get("colors", {}).get("secondaryHex", None)
        cache[team.team] = {
            "primary": team.primary_color,
            "secondary": team.secondary_color,
        }

        if len(cache) % 100 == 0:
            print("Writing cache")
            with open("cache/colors.json", "w") as f:
                dump(cache, f)

    return teams
