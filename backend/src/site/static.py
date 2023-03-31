import json
from typing import Dict, List

# read the file
with open("data/epa_breakdown.json") as f:
    epa_breakdown = json.load(f)


def get_epa_breakdown(teams: List[int]) -> Dict[int, Dict[str, float]]:
    return {team: epa_breakdown[str(team)] for team in teams}
