from typing import Any, Dict, List, Optional

from helper.utils import load
from tba.config import get_tba

USA = {
    "Alabama": "AL",
    "Alaska": "AK",
    "American Samoa": "AS",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "District of Columbia": "DC",
    "Florida": "FL",
    "Georgia": "GA",
    "Guam": "GU",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Northern Mariana Islands": "MP",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Puerto Rico": "PR",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virgin Islands": "VI",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
}

Canada = {
    "Newfoundland": "NL",
    "Prince Edward Island": "PE",
    "Nova Scotia": "NS",
    "New Brunswick": "NB",
    "Québec": "QC",
    "Ontario": "ON",
    "Manitoba": "MB",
    "Saskatchewan": "SK",
    "Alberta": "AB",
    "British Columbia": "BC",
    "Yukon": "YT",
    "Northwest Territories": "NT",
    "Nunavut": "NU",
}

districts = {
    "mar": "fma",
    "nc": "fnc",
    "tx": "fit",
    "in": "fin",
}


def get_team_info(number: int) -> List[Any]:
    data = get_tba("team/frc" + str(number) + "/simple")
    name = data["nickname"]
    state = data["state_prov"]
    country = data["country"]

    years = len(get_tba("team/frc" + str(number) + "/years_participated"))

    try:
        district = get_tba("team/frc" + str(number) + "/districts")[-1]["abbreviation"]
    except Exception:
        district = "None"

    if state in USA:
        state = USA[state]
    elif state in Canada:
        state = Canada[state]
    elif country != "USA" and country != "Canada":
        state = "All"

    if district in districts:
        district = districts[district]

    return [name, country, state, district, years]


def clean_state(state: str) -> str:
    if state in USA:
        return USA[state]
    if state in Canada:
        return Canada[state]
    if state in USA.values():
        return state
    if state in Canada.values():
        return state
    return "All"


def clean_district(district: str) -> str:
    if district in districts:
        return districts[district]
    return district


teams_info: Any = load("teams_info.p")


def get_team_district(team: int):
    return teams_info[team][3]


def get_match_time(match: Dict[str, Any], event_time: int) -> int:
    if match["actual_time"] is not None:
        return match["actual_time"]

    match_time = event_time  # start value
    if match["comp_level"] == "qm":
        match_time += match["match_number"]
    elif match["comp_level"] == "qf":
        match_time += 200 + 10 * match["set_number"] + match["match_number"]
    elif match["comp_level"] == "sf":
        match_time += 400 + 10 * match["set_number"] + match["match_number"]
    else:
        match_time += 600 + match["match_number"]
    return match_time


def get_breakdown(
    year: int, breakdown: Optional[Dict[str, Any]] = None
) -> Dict[str, Optional[int]]:
    out: Dict[str, Optional[int]] = {}
    if breakdown is None or year < 2016:
        out = {
            "auto": None,
            "auto_movement": None,
            "auto_1": None,
            "auto_2": None,
            "teleop_1": None,
            "teleop_2": None,
            "1": None,
            "2": None,
            "teleop": None,
            "endgame": None,
            "no_fouls": None,
            "fouls": None,
            "rp1": None,
            "rp2": None,
        }
        return out
    if year == 2016:
        out = {
            "auto": breakdown["autoPoints"],
            "auto_movement": breakdown["autoReachPoints"],
            "auto_1": breakdown["autoCrossingPoints"],
            "auto_2": breakdown["autoBoulderPoints"],
            "teleop_1": breakdown["teleopCrossingPoints"],
            "teleop_2": breakdown["teleopBoulderPoints"],
        }
        out["1"] = out["auto_1"] + out["teleop_1"]  # type: ignore
        out["2"] = out["auto_2"] + out["teleop_2"]  # type: ignore
        out["teleop"] = out["teleop_1"] + out["teleop_2"]  # type: ignore
        out["endgame"] = breakdown["teleopChallengePoints"]
        out["no_fouls"] = out["auto"] + out["teleop"] + out["endgame"]  # type: ignore
        out["fouls"] = breakdown["foulPoints"]
        out["rp1"] = 1 if breakdown["teleopDefensesBreached"] else 0
        out["rp2"] = 1 if breakdown["teleopTowerCaptured"] else 0
        return out
    if year == 2017:
        out = {
            "auto": breakdown["autoPoints"],
            "auto_movement": breakdown["autoMobilityPoints"],
            "auto_1": breakdown["autoRotorPoints"],
            "auto_2": breakdown["autoFuelPoints"],
            "teleop_1": breakdown["teleopRotorPoints"],
            "teleop_2": breakdown["teleopFuelPoints"],
        }
        out["1"] = out["auto_1"] + out["teleop_1"]  # type: ignore
        out["2"] = out["auto_2"] + out["teleop_2"]  # type: ignore
        out["teleop"] = out["teleop_1"] + out["teleop_2"]  # type: ignore
        out["endgame"] = breakdown["teleopTakeoffPoints"]
        out["no_fouls"] = out["auto"] + out["teleop"] + out["endgame"]  # type: ignore
        out["fouls"] = breakdown["foulPoints"]
        out["rp1"] = 1 if breakdown["rotorRankingPointAchieved"] else 0
        out["rp2"] = 1 if breakdown["kPaRankingPointAchieved"] else 0
        return out
    if year == 2018:
        out = {
            "auto": breakdown["autoPoints"],
            "auto_movement": breakdown["autoRunPoints"],
            "auto_1": 0,
            "auto_2": breakdown["autoOwnershipPoints"],
            "teleop_1": breakdown["vaultPoints"],
            "teleop_2": breakdown["teleopOwnershipPoints"],
        }
        out["1"] = out["auto_1"] + out["teleop_1"]  # type: ignore
        out["2"] = out["auto_2"] + out["teleop_2"]  # type: ignore
        out["teleop"] = out["teleop_1"] + out["teleop_2"]  # type: ignore
        out["endgame"] = breakdown["endgamePoints"]
        out["no_fouls"] = out["auto"] + out["teleop"] + out["endgame"]  # type: ignore
        out["fouls"] = breakdown["foulPoints"]
        out["rp1"] = 1 if breakdown["autoQuestRankingPoint"] else 0
        out["rp2"] = 1 if breakdown["faceTheBossRankingPoint"] else 0
        return out
    if year == 2019:
        out = {
            "auto": breakdown["autoPoints"],
            "auto_movement": breakdown["sandStormBonusPoints"],
            "auto_1": 0,
            "auto_2": 0,
            "teleop_1": breakdown["hatchPanelPoints"],
            "teleop_2": breakdown["cargoPoints"],
        }
        out["1"] = out["auto_1"] + out["teleop_1"]  # type: ignore
        out["2"] = out["auto_2"] + out["teleop_2"]  # type: ignore
        out["teleop"] = out["teleop_1"] + out["teleop_2"]  # type: ignore
        out["endgame"] = breakdown["habClimbPoints"]
        out["no_fouls"] = out["auto"] + out["teleop"] + out["endgame"]  # type: ignore
        out["fouls"] = breakdown["foulPoints"]
        out["rp1"] = 1 if breakdown["completeRocketRankingPoint"] else 0
        out["rp2"] = 1 if breakdown["habDockingRankingPoint"] else 0
        return out
    if year == 2020:
        out = {
            "auto": breakdown["autoPoints"],
            "auto_movement": breakdown["autoInitLinePoints"],
            "auto_1": 0,
            "auto_2": breakdown["autoCellPoints"],
            "teleop_1": breakdown["controlPanelPoints"],
            "teleop_2": breakdown["teleopCellPoints"],
        }
        out["1"] = out["auto_1"] + out["teleop_1"]  # type: ignore
        out["2"] = out["auto_2"] + out["teleop_2"]  # type: ignore
        out["teleop"] = out["teleop_1"] + out["teleop_2"]  # type: ignore
        out["endgame"] = breakdown["endgamePoints"]
        out["no_fouls"] = out["auto"] + out["teleop"] + out["endgame"]  # type: ignore
        out["fouls"] = breakdown["foulPoints"]
        out["rp1"] = 1 if breakdown["shieldEnergizedRankingPoint"] else 0
        out["rp2"] = 1 if breakdown["shieldOperationalRankingPoint"] else 0
        return out
    return {}
