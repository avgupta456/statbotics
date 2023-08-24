from typing import Any, Dict, Optional

from src.tba.types import BreakdownDict


empty_breakdown: BreakdownDict = {
    "score": None,
    "no_foul_points": None,
    "foul_points": None,
    "auto_points": None,
    "teleop_points": None,
    "endgame_points": None,
    "rp_1": None,
    "rp_2": None,
    "comp_1": None,
    "comp_2": None,
    "comp_3": None,
    "comp_4": None,
    "comp_5": None,
    "comp_6": None,
    "comp_7": None,
    "comp_8": None,
    "comp_9": None,
    "comp_10": None,
    "tiebreaker": None,
}

INVALID_MATCH_KEYS = ["2016capl_f1m1", "2016milsu_qf4m1", "2016mndu2_f1m2"]


def clean_breakdown_2016(
    key: str,
    breakdown: Dict[str, Any],
    opp_breakdown: Dict[str, Any],
    score: int,
    no_foul_points: int,
    foul_points: int,
) -> BreakdownDict:
    auto_reach_points = breakdown.get("autoReachPoints", 0)
    auto_crossing_points = breakdown.get("autoCrossingPoints", 0)
    auto_low_boulders = breakdown.get("autoBouldersLow", 0)
    auto_high_boulders = breakdown.get("autoBouldersHigh", 0)

    # some 2016 offseason events don't have autoBouldersLow/High
    auto_boulder_points = breakdown.get("autoBoulderPoints", 0)
    if 5 * auto_low_boulders + 10 * auto_high_boulders != auto_boulder_points:
        # print("Auto Boulders", key)
        auto_high_boulders = auto_boulder_points // 10
        auto_low_boulders = (auto_boulder_points - 10 * auto_high_boulders) // 5

    teleop_crossing_points = breakdown.get("teleopCrossingPoints", 0)
    teleop_low_boulders = breakdown.get("teleopBouldersLow", 0)
    teleop_high_boulders = breakdown.get("teleopBouldersHigh", 0)

    challenge_points = breakdown.get("teleopChallengePoints", 0)
    scale_points = breakdown.get("teleopScalePoints", 0)

    auto_points = (
        auto_reach_points
        + auto_crossing_points
        + 5 * auto_low_boulders
        + 10 * auto_high_boulders
    )

    teleop_points = (
        teleop_crossing_points + 2 * teleop_low_boulders + 5 * teleop_high_boulders
    )

    endgame_points = challenge_points + scale_points

    rp_1 = bool(breakdown.get("teleopDefensesBreached", 0))
    rp_2 = bool(breakdown.get("teleopTowerCaptured", 0))

    rp_1_points = breakdown.get("breachPoints", 0)
    rp_2_points = breakdown.get("capturePoints", 0)
    no_foul_points -= rp_1_points + rp_2_points

    tiebreaker = -opp_breakdown.get("foulPoints", 0)

    return {
        "score": score,
        "no_foul_points": no_foul_points,
        "foul_points": foul_points,
        "auto_points": auto_points,
        "teleop_points": teleop_points,
        "endgame_points": endgame_points,
        "rp_1": rp_1,
        "rp_2": rp_2,
        "comp_1": auto_reach_points,
        "comp_2": auto_crossing_points,
        "comp_3": auto_low_boulders,
        "comp_4": auto_high_boulders,
        "comp_5": teleop_crossing_points,
        "comp_6": teleop_low_boulders,
        "comp_7": teleop_high_boulders,
        "comp_8": challenge_points,
        "comp_9": scale_points,
        "comp_10": 0,
        "tiebreaker": tiebreaker,
    }


def clean_breakdown(
    year: int,
    offseason: bool,
    key: str,
    breakdown: Optional[Dict[str, Any]],
    opp_breakdown: Optional[Dict[str, Any]],
    score: Optional[int],
) -> BreakdownDict:
    out = empty_breakdown
    if breakdown is None or opp_breakdown is None or score is None or year < 2016:
        return out

    # Shared
    foul_points = breakdown.get("foulPoints", 0) + breakdown.get("adjustPoints", 0)
    no_foul_points = score - foul_points

    inputs = (key, breakdown, opp_breakdown, score, no_foul_points, foul_points)

    if year == 2016:
        out = clean_breakdown_2016(*inputs)
    else:
        out["no_foul_points"] = score

    if year >= 2016 and key not in INVALID_MATCH_KEYS:
        auto_points = out["auto_points"] or 0
        teleop_points = out["teleop_points"] or 0
        endgame_points = out["endgame_points"] or 0
        no_foul_points = out["no_foul_points"] or 0
        if auto_points + teleop_points + endgame_points != no_foul_points:
            print(key, auto_points, teleop_points, endgame_points, no_foul_points)
            if not offseason:
                assert auto_points + teleop_points + endgame_points == no_foul_points

    return out

    """
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
        a, b, c = int(out["auto_2_1"]), int(out["auto_2_2"]), int(out["auto_2"])
        if a + b != c:
            out["auto_2_1" if a > b else "auto_2_2"] = c - min(a, b)

        a, b, c = int(out["teleop_2_1"]), int(out["teleop_2_2"]), int(out["teleop_2"])
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
        a, b, c = int(out["auto_2_1"]), int(out["auto_2_2"]), int(out["auto_2"])
        if a + b != c:
            out["auto_2_1" if a > b else "auto_2_2"] = c - min(a, b)

        a, b, c = int(out["teleop_2_1"]), int(out["teleop_2_2"]), int(out["teleop_2"])
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
            # first tiebreaker is average alliance match score, not including fouls
            "tiebreaker": breakdown.get("autoPoints", 0)
            + breakdown.get("teleopGamePiecePoints", 0)
            + breakdown.get("linkPoints", 0)
            + breakdown.get("endGameChargeStationPoints", 0)
            + breakdown.get("endGameParkPoints", 0),
        }
    else:
        raise ValueError("Invalid year: " + str(year))

    out["1"] = out["auto_1"] + out["teleop_1"]
    out["2"] = out["auto_2"] + out["teleop_2"]
    out["teleop"] = out["teleop_1"] + out["teleop_2"]
    out["no_foul"] = out["auto"] + out["teleop"] + out["endgame"]
    out["foul"] = breakdown.get("foulPoints", 0)
    return out
    """
