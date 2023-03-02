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


def get_breakdown(
    year: int,
    breakdown: Optional[Dict[str, Any]] = None,
    opp_breakdown: Optional[Dict[str, Any]] = None,
) -> Dict[str, Optional[int]]:
    out: Dict[str, Optional[int]] = {}
    if breakdown is None or opp_breakdown is None or year < 2016:
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
            "tiebreaker": None,
        }

    if year == 2016:
        out = {
            "auto": breakdown.get("autoPoints", 0),
            "auto_movement": breakdown.get("autoReachPoints", 0),
            "auto_1": breakdown.get("autoCrossingPoints", 0),
            "auto_2": breakdown.get("autoBoulderPoints", 0),
            "auto_2_1": 5 * breakdown.get("autoBouldersLow", 0),
            "auto_2_2": 10 * breakdown.get("autoBouldersHigh", 0),
            "teleop_1": breakdown.get("teleopCrossingPoints", 0),
            "teleop_2": breakdown.get("teleopBoulderPoints", 0),
            "teleop_2_1": 2 * breakdown.get("teleopBouldersLow", 0),
            "teleop_2_2": 5 * breakdown.get("teleopBouldersHigh", 0),
            "endgame": breakdown.get("teleopChallengePoints", 0)
            + breakdown.get("teleopScalePoints", 0),
            "rp1": int(breakdown.get("teleopDefensesBreached", 0)),
            "rp2": int(breakdown.get("teleopTowerCaptured", 0)),
            "tiebreaker": -opp_breakdown.get("foulPoints", 0),
        }
    elif year == 2017:
        out = {
            "auto": breakdown.get("autoPoints", 0),
            "auto_movement": breakdown.get("autoMobilityPoints", 0),
            "auto_1": breakdown.get("autoRotorPoints", 0),
            "auto_2": breakdown.get("autoFuelPoints", 0),
            "auto_2_1": breakdown.get("autoFuelLow", 0) // 3,
            "auto_2_2": breakdown.get("autoFuelHigh", 0),
            "teleop_1": breakdown.get("teleopRotorPoints", 0),
            "teleop_2": breakdown.get("teleopFuelPoints", 0),
            "teleop_2_1": breakdown.get("teleopFuelLow", 0) // 9,
            "teleop_2_2": breakdown.get("teleopFuelHigh", 0) // 3,
            "endgame": breakdown.get("teleopTakeoffPoints", 0),
            "rp1": int(breakdown.get("rotorRankingPointAchieved", 0)),
            "rp2": int(breakdown.get("kPaRankingPointAchieved", 0)),
            "tiebreaker": breakdown.get("autoPoints", 0),
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
            "auto": breakdown.get("autoPoints", 0),
            "auto_movement": breakdown.get("autoRunPoints", 0),
            "auto_1": 0,
            "auto_2": breakdown.get("autoOwnershipPoints", 0),
            "auto_2_1": 2 * breakdown.get("autoSwitchOwnershipSec", 0),
            "auto_2_2": 2 * breakdown.get("autoScaleOwnershipSec", 0),
            "teleop_1": breakdown.get("vaultPoints", 0),
            "teleop_2": breakdown.get("teleopOwnershipPoints", 0),
            "teleop_2_1": breakdown.get("teleopSwitchOwnershipSec", 0)
            + breakdown.get("teleopSwitchBoostSec", 0),
            "teleop_2_2": breakdown.get("teleopScaleOwnershipSec", 0)
            + breakdown.get("teleopScaleBoostSec", 0),
            "endgame": breakdown.get("endgamePoints", 0),
            "rp1": int(breakdown.get("autoQuestRankingPoint", 0)),
            "rp2": int(breakdown.get("faceTheBossRankingPoint", 0)),
            "tiebreaker": breakdown.get("endgamePoints", 0),
        }
    elif year == 2019:
        out = {
            "auto": breakdown.get("autoPoints", 0),
            "auto_movement": breakdown.get("sandStormBonusPoints", 0),
            "auto_1": 0,
            "auto_2": 0,
            "auto_2_1": 0,
            "auto_2_2": 0,
            "teleop_1": breakdown.get("hatchPanelPoints", 0),
            "teleop_2": breakdown.get("cargoPoints", 0),
            "teleop_2_1": 0,
            "teleop_2_2": 0,
            "endgame": breakdown.get("habClimbPoints", 0),
            "rp1": int(breakdown.get("completeRocketRankingPoint", 0)),
            "rp2": int(breakdown.get("habDockingRankingPoint", 0)),
            "tiebreaker": breakdown.get("cargoPoints", 0),
        }
    elif year == 2020:
        out = {
            "auto": breakdown.get("autoPoints", 0),
            "auto_movement": breakdown.get("autoInitLinePoints", 0),
            "auto_1": 0,
            "auto_2": breakdown.get("autoCellPoints", 0),
            "auto_2_1": 2 * breakdown.get("autoCellsBottom", 0),
            "auto_2_2": 4 * breakdown.get("autoCellsOuter", 0)
            + 6 * breakdown.get("autoCellsInner", 0),
            "teleop_1": breakdown.get("controlPanelPoints", 0),
            "teleop_2": breakdown.get("teleopCellPoints", 0),
            "teleop_2_1": breakdown.get("teleopCellsBottom", 0),
            "teleop_2_2": 2 * breakdown.get("teleopCellsOuter", 0)
            + 3 * breakdown.get("teleopCellsInner", 0),
            "endgame": breakdown.get("endgamePoints", 0),
            "rp1": int(breakdown.get("shieldEnergizedRankingPoint", 0)),
            "rp2": int(breakdown.get("shieldOperationalRankingPoint", 0)),
            "tiebreaker": breakdown.get("autoPoints", 0),
        }
    elif year == 2021:
        return {}
    elif year == 2022:
        out = {
            "auto": breakdown.get("autoPoints", 0),
            "auto_movement": breakdown.get("autoTaxiPoints", 0),
            "auto_1": 0,
            "auto_2": breakdown.get("autoCargoPoints", 0),
            "auto_2_1": breakdown.get("autoCargoLowerBlue", 0)
            + breakdown.get("autoCargoLowerRed", 0)
            + breakdown.get("autoCargoLowerFar", 0)
            + breakdown.get("autoCargoLowerNear", 0),
            "auto_2_2": breakdown.get("autoCargoUpperBlue", 0)
            + breakdown.get("autoCargoUpperRed", 0)
            + breakdown.get("autoCargoUpperFar", 0)
            + breakdown.get("autoCargoUpperNear", 0),
            "teleop_1": 0,
            "teleop_2": breakdown.get("teleopCargoPoints", 0),
            "teleop_2_1": breakdown.get("teleopCargoLowerBlue", 0)
            + breakdown.get("teleopCargoLowerRed", 0)
            + breakdown.get("teleopCargoLowerFar", 0)
            + breakdown.get("teleopCargoLowerNear", 0),
            "teleop_2_2": 2
            * (
                breakdown.get("teleopCargoUpperBlue", 0)
                + breakdown.get("teleopCargoUpperRed", 0)
                + breakdown.get("teleopCargoUpperFar", 0)
                + breakdown.get("teleopCargoUpperNear", 0)
            ),
            "endgame": breakdown.get("endgamePoints", 0),
            "rp1": int(breakdown.get("cargoBonusRankingPoint", 0)),
            "rp2": int(breakdown.get("hangarBonusRankingPoint", 0)),
            "tiebreaker": breakdown.get("autoPoints", 0)
            + breakdown.get("teleopCargoPoints", 0)
            + breakdown.get("endgamePoints", 0)
            + breakdown.get("foulPoints", 0),
        }

        # Correct some edge cases (sensor issues, etc.)
        a, b, c = int(out["auto_2_1"]), int(out["auto_2_2"]), int(out["auto_2"])  # type: ignore
        if a + b != c:
            out["auto_2_1" if a > b else "auto_2_2"] = c - min(a, b)

        a, b, c = int(out["teleop_2_1"]), int(out["teleop_2_2"]), int(out["teleop_2"])  # type: ignore
        if a + b != c:
            out["teleop_2_1" if a > b else "teleop_2_2"] = c - min(a, b)
    elif year == 2023:
        out = {
            "auto": breakdown.get("autoPoints", 0),
            "auto_movement": breakdown.get("autoMobilityPoints", 0),
            "auto_1": breakdown.get("autoChargeStationPoints", 0),
            "auto_2": breakdown.get("autoGamePiecePoints", 0),
            "auto_2_1": breakdown.get("autoGamePiecePoints", 0),
            "auto_2_2": 0,
            "teleop_1": 0,
            "teleop_2": breakdown.get("teleopGamePiecePoints", 0)
            + breakdown.get("linkPoints", 0),
            "teleop_2_1": breakdown.get("teleopGamePiecePoints"),
            "teleop_2_2": breakdown.get("linkPoints"),
            "endgame": breakdown.get("endGameChargeStationPoints", 0)
            + breakdown.get("endGameParkPoints", 0),
            "rp1": int(breakdown.get("sustainabilityBonusAchieved", 0)),
            "rp2": int(breakdown.get("activationBonusAchieved", 0)),
            # first tiebreaker is tech foul count, second is charge station points
            "tiebreaker": 10000 * breakdown.get("techFoulCount", 0)
            + breakdown.get("totalChargeStationPoints", 0),
        }
    else:
        raise ValueError("Invalid year: " + str(year))

    out["1"] = out["auto_1"] + out["teleop_1"]  # type: ignore
    out["2"] = out["auto_2"] + out["teleop_2"]  # type: ignore
    out["teleop"] = out["teleop_1"] + out["teleop_2"]  # type: ignore
    out["no_fouls"] = out["auto"] + out["teleop"] + out["endgame"]  # type: ignore
    out["fouls"] = breakdown.get("foulPoints", 0)
    return out
