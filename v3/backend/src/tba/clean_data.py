from typing import Optional

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


def get_match_time(
    comp_level: str, set_number: int, match_number: int, event_time: int
) -> int:
    match_time = event_time  # start value
    if comp_level == "qm":
        match_time += match_number
    elif comp_level == "ef":
        match_time += 200 + 10 * set_number + match_number
    elif comp_level == "qf":
        match_time += 300 + 10 * set_number + match_number
    elif comp_level == "sf":
        match_time += 400 + 10 * set_number + match_number
    elif comp_level == "f":
        match_time += 500 + match_number
    else:
        raise ValueError("Invalid comp_level: " + comp_level)
    return match_time
