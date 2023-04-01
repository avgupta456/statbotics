import json
from typing import Dict, List

# read the file
with open("data/epa_breakdown.json") as f:
    epa_breakdown = json.load(f)

with open("data/event_epa_breakdown.json") as f:
    event_epa_breakdown = json.load(f)

with open("data/epa_breakdown_percentiles.json") as f:
    epa_breakdown_percentiles = json.load(f)


def get_epa_breakdown(teams: List[int]) -> Dict[int, Dict[str, float]]:
    return {team: epa_breakdown.get(str(team), {}) for team in teams}


def get_event_epa_breakdown(event_key: str) -> Dict[int, Dict[str, float]]:
    valid_keys = [k for k in event_epa_breakdown.keys() if k.endswith("_" + event_key)]
    return {int(k.split("_")[0]): event_epa_breakdown[k] for k in valid_keys}


def get_epa_breakdown_percentiles() -> Dict[str, Dict[str, float]]:
    return epa_breakdown_percentiles
