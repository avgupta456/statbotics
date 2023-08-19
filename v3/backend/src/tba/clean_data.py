from typing import Any, Dict, Optional

from src.tba.constants import CANADA_MAPPING, DISTRICT_MAPPING, USA_MAPPING


def clean_state(state: str) -> Optional[str]:
    if state in USA_MAPPING:
        return USA_MAPPING[state]
    if state in CANADA_MAPPING:
        return CANADA_MAPPING[state]
    if state in USA_MAPPING.values():
        return state
    if state in CANADA_MAPPING.values():
        return state
    return None


def clean_district(district: Optional[str]) -> Optional[str]:
    if district in DISTRICT_MAPPING:
        return DISTRICT_MAPPING[district]
    return district


def get_match_time(match: Dict[str, Any], event_time: int) -> int:
    match_time = event_time  # start value
    if match["comp_level"] == "qm":
        match_time += match["match_number"]
    elif match["comp_level"] == "ef":
        match_time += 200 + 10 * match["set_number"] + match["match_number"]
    elif match["comp_level"] == "qf":
        match_time += 300 + 10 * match["set_number"] + match["match_number"]
    elif match["comp_level"] == "sf":
        match_time += 400 + 10 * match["set_number"] + match["match_number"]
    elif match["comp_level"] == "f":
        match_time += 500 + match["match_number"]
    else:
        raise ValueError("Invalid comp_level: " + match["comp_level"])
    return match_time
