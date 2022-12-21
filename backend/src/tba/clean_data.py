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
        return {
            "auto": None,
            "auto_movement": None,
            "auto_1": None,
            "auto_2": None,
            "auto_2_1": None,
            "auto_2_2": None,
            "teleop_1": None,
            "teleop_2": None,
            "teleop_2_1": None,
            "teleop_2_2": None,
            "1": None,
            "2": None,
            "teleop": None,
            "endgame": None,
            "no_fouls": None,
            "fouls": None,
            "rp1": None,
            "rp2": None,
        }

    if year == 2016:
        out = {
            "auto": breakdown["autoPoints"],
            "auto_movement": breakdown["autoReachPoints"],
            "auto_1": breakdown["autoCrossingPoints"],
            "auto_2": breakdown["autoBoulderPoints"],
            "auto_2_1": 5 * breakdown["autoBouldersLow"],
            "auto_2_2": 10 * breakdown["autoBouldersHigh"],
            "teleop_1": breakdown["teleopCrossingPoints"],
            "teleop_2": breakdown["teleopBoulderPoints"],
            "teleop_2_1": 2 * breakdown["teleopBouldersLow"],
            "teleop_2_2": 5 * breakdown["teleopBouldersHigh"],
            "endgame": breakdown["teleopChallengePoints"]
            + breakdown["teleopScalePoints"],
            "rp1": int(breakdown["teleopDefensesBreached"]),
            "rp2": int(breakdown["teleopTowerCaptured"]),
        }
    elif year == 2017:
        out = {
            "auto": breakdown["autoPoints"],
            "auto_movement": breakdown["autoMobilityPoints"],
            "auto_1": breakdown["autoRotorPoints"],
            "auto_2": breakdown["autoFuelPoints"],
            "auto_2_1": breakdown["autoFuelLow"] // 3,
            "auto_2_2": breakdown["autoFuelHigh"],
            "teleop_1": breakdown["teleopRotorPoints"],
            "teleop_2": breakdown["teleopFuelPoints"],
            "teleop_2_1": breakdown["teleopFuelLow"] // 9,
            "teleop_2_2": breakdown["teleopFuelHigh"] // 3,
            "endgame": breakdown["teleopTakeoffPoints"],
            "rp1": int(breakdown["rotorRankingPointAchieved"]),
            "rp2": int(breakdown["kPaRankingPointAchieved"]),
        }

        # Correct some off-by-one edge cases
        a, b, c = int(out["auto_2_1"]), int(out["auto_2_2"]), int(out["auto_2"])  # type: ignore
        if a + b != c:
            out["auto_2_1" if a > b else "auto_2_2"] = c - min(a, b)

        a, b, c = int(out["teleop_2_1"]), int(out["teleop_2_2"]), int(out["teleop_2"])  # type: ignore
        if a + b != c:
            out["teleop_2_1" if a > b else "teleop_2_2"] = c - min(a, b)

    elif year == 2018:
        out = {
            "auto": breakdown["autoPoints"],
            "auto_movement": breakdown["autoRunPoints"],
            "auto_1": 0,
            "auto_2": breakdown["autoOwnershipPoints"],
            "auto_2_1": 2 * breakdown["autoSwitchOwnershipSec"],
            "auto_2_2": 2 * breakdown["autoScaleOwnershipSec"],
            "teleop_1": breakdown["vaultPoints"],
            "teleop_2": breakdown["teleopOwnershipPoints"],
            "teleop_2_1": breakdown["teleopSwitchOwnershipSec"]
            + breakdown["teleopSwitchBoostSec"],
            "teleop_2_2": breakdown["teleopScaleOwnershipSec"]
            + breakdown["teleopScaleBoostSec"],
            "endgame": breakdown["endgamePoints"],
            "rp1": int(breakdown["autoQuestRankingPoint"]),
            "rp2": int(breakdown["faceTheBossRankingPoint"]),
        }
    elif year == 2019:
        out = {
            "auto": breakdown["autoPoints"],
            "auto_movement": breakdown["sandStormBonusPoints"],
            "auto_1": 0,
            "auto_2": 0,
            "auto_2_1": 0,
            "auto_2_2": 0,
            "teleop_1": breakdown["hatchPanelPoints"],
            "teleop_2": breakdown["cargoPoints"],
            "teleop_2_1": 0,
            "teleop_2_2": 0,
            "endgame": breakdown["habClimbPoints"],
            "rp1": int(breakdown["completeRocketRankingPoint"]),
            "rp2": int(breakdown["habDockingRankingPoint"]),
        }
    elif year == 2020:
        out = {
            "auto": breakdown["autoPoints"],
            "auto_movement": breakdown["autoInitLinePoints"],
            "auto_1": 0,
            "auto_2": breakdown["autoCellPoints"],
            "auto_2_1": 2 * breakdown["autoCellsBottom"],
            "auto_2_2": 4 * breakdown["autoCellsOuter"]
            + 6 * breakdown["autoCellsInner"],
            "teleop_1": breakdown["controlPanelPoints"],
            "teleop_2": breakdown["teleopCellPoints"],
            "teleop_2_1": breakdown["teleopCellsBottom"],
            "teleop_2_2": 2 * breakdown["teleopCellsOuter"]
            + 3 * breakdown["teleopCellsInner"],
            "endgame": breakdown["endgamePoints"],
            "rp1": int(breakdown["shieldEnergizedRankingPoint"]),
            "rp2": int(breakdown["shieldOperationalRankingPoint"]),
        }
    elif year == 2021:
        return {}
    elif year == 2022:
        out = {
            "auto": breakdown["autoPoints"],
            "auto_movement": breakdown["autoTaxiPoints"],
            "auto_1": 0,
            "auto_2": breakdown["autoCargoPoints"],
            "auto_2_1": breakdown["autoCargoLowerBlue"]
            + breakdown["autoCargoLowerRed"]
            + breakdown["autoCargoLowerFar"]
            + breakdown["autoCargoLowerNear"],
            "auto_2_2": breakdown["autoCargoUpperBlue"]
            + breakdown["autoCargoUpperRed"]
            + breakdown["autoCargoUpperFar"]
            + breakdown["autoCargoUpperNear"],
            "teleop_1": 0,
            "teleop_2": breakdown["teleopCargoPoints"],
            "teleop_2_1": breakdown["teleopCargoLowerBlue"]
            + breakdown["teleopCargoLowerRed"]
            + breakdown["teleopCargoLowerFar"]
            + breakdown["teleopCargoLowerNear"],
            "teleop_2_2": 2
            * (
                breakdown["teleopCargoUpperBlue"]
                + breakdown["teleopCargoUpperRed"]
                + breakdown["teleopCargoUpperFar"]
                + breakdown["teleopCargoUpperNear"]
            ),
            "endgame": breakdown["endgamePoints"],
            "rp1": int(breakdown["cargoBonusRankingPoint"]),
            "rp2": int(breakdown["hangarBonusRankingPoint"]),
        }

        # Correct some edge cases (sensor issues, etc.)
        a, b, c = int(out["auto_2_1"]), int(out["auto_2_2"]), int(out["auto_2"])  # type: ignore
        if a + b != c:
            out["auto_2_1" if a > b else "auto_2_2"] = c - min(a, b)

        a, b, c = int(out["teleop_2_1"]), int(out["teleop_2_2"]), int(out["teleop_2"])  # type: ignore
        if a + b != c:
            out["teleop_2_1" if a > b else "teleop_2_2"] = c - min(a, b)

    out["1"] = out["auto_1"] + out["teleop_1"]  # type: ignore
    out["2"] = out["auto_2"] + out["teleop_2"]  # type: ignore
    out["teleop"] = out["teleop_1"] + out["teleop_2"]  # type: ignore
    out["no_fouls"] = out["auto"] + out["teleop"] + out["endgame"]  # type: ignore
    out["fouls"] = breakdown["foulPoints"]
    return out
