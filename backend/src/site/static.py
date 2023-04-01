import json
from typing import Dict, List

# read the file
with open("data/epa_breakdown.json") as f:
    epa_breakdown = json.load(f)

with open("data/epa_breakdown_percentiles.json") as f:
    epa_breakdown_percentiles = json.load(f)


def get_epa_breakdown(teams: List[int]) -> Dict[int, Dict[str, float]]:
    return {team: epa_breakdown.get(str(team), {}) for team in teams}


def get_epa_breakdown_percentiles() -> Dict[str, Dict[str, float]]:
    return epa_breakdown_percentiles
