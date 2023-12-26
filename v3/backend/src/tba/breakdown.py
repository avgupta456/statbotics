from typing import Any, Dict, List, Optional

from src.tba.types import BreakdownDict

empty_breakdown: BreakdownDict = {
    "score": 0,
    "no_foul_points": None,
    "foul_points": None,
    "auto_points": None,
    "teleop_points": None,
    "endgame_points": None,
    "rp_1": False,
    "rp_2": False,
    "tiebreaker": None,
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
    "comp_11": None,
    "comp_12": None,
}

INVALID_MATCH_KEYS = ["2016capl_f1m1", "2016milsu_qf4m1", "2016mndu2_f1m2"]


def clean_breakdown_2016(
    key: str,
    breakdown: Dict[str, Any],
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
        auto_high_boulders = auto_boulder_points // 10
        auto_low_boulders = (auto_boulder_points - 10 * auto_high_boulders) // 5

    teleop_crossing_points = breakdown.get("teleopCrossingPoints", 0)
    teleop_low_boulders = breakdown.get("teleopBouldersLow", 0)
    teleop_high_boulders = breakdown.get("teleopBouldersHigh", 0)

    challenge_points = breakdown.get("teleopChallengePoints", 0)
    scale_points = breakdown.get("teleopScalePoints", 0)

    defenses = auto_crossing_points / 10 + teleop_crossing_points / 5
    boulders = (
        auto_low_boulders
        + auto_high_boulders
        + teleop_low_boulders
        + teleop_high_boulders
    )

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

    rp_1 = bool(breakdown.get("teleopDefensesBreached", False))
    rp_2 = bool(breakdown.get("teleopTowerCaptured", False))

    rp_1_points = breakdown.get("breachPoints", 0)
    rp_2_points = breakdown.get("capturePoints", 0)
    no_foul_points -= rp_1_points + rp_2_points

    tiebreaker = breakdown.get("autoPoints", 0)

    return {
        "score": score,
        "no_foul_points": no_foul_points,
        "foul_points": foul_points,
        "auto_points": auto_points,
        "teleop_points": teleop_points,
        "endgame_points": endgame_points,
        "rp_1": rp_1,
        "rp_2": rp_2,
        "tiebreaker": tiebreaker,
        "comp_1": auto_reach_points,
        "comp_2": auto_crossing_points,
        "comp_3": auto_low_boulders,
        "comp_4": auto_high_boulders,
        "comp_5": teleop_crossing_points,
        "comp_6": teleop_low_boulders,
        "comp_7": teleop_high_boulders,
        "comp_8": challenge_points,
        "comp_9": scale_points,
        "comp_10": defenses,
        "comp_11": boulders,
        "comp_12": 0,
    }


def clean_breakdown_2017(
    key: str,
    breakdown: Dict[str, Any],
    score: int,
    no_foul_points: int,
    foul_points: int,
) -> BreakdownDict:
    auto_mobility_points = breakdown.get("autoMobilityPoints", 0)
    auto_fuel_low = breakdown.get("autoFuelLow", 0)
    auto_fuel_high = breakdown.get("autoFuelHigh", 0)
    auto_rotor_points = breakdown.get("autoRotorPoints", 0)

    teleop_fuel_low = breakdown.get("teleopFuelLow", 0)
    teleop_fuel_high = breakdown.get("teleopFuelHigh", 0)
    teleop_rotor_points = breakdown.get("teleopRotorPoints", 0)

    num_auto_rotors = auto_rotor_points // 60
    auto_rotor_points -= 40 * num_auto_rotors
    teleop_rotor_points += 40 * num_auto_rotors

    takeoff_points = breakdown.get("teleopTakeoffPoints", 0)

    auto_kpa_9ths = 3 * auto_fuel_low + 9 * auto_fuel_high
    auto_points = auto_mobility_points + auto_rotor_points + auto_kpa_9ths // 9

    teleop_kpa_9ths = auto_kpa_9ths % 9 + teleop_fuel_low + 3 * teleop_fuel_high
    teleop_points = teleop_rotor_points + teleop_kpa_9ths // 9

    rp_1 = bool(breakdown.get("kPaRankingPointAchieved", False))
    rp_2 = bool(breakdown.get("rotorRankingPointAchieved", False))

    rp_1_points = breakdown.get("kPaBonusPoints", 0)
    rp_2_points = breakdown.get("rotorBonusPoints", 0)

    no_foul_points -= rp_1_points + rp_2_points

    tiebreaker = no_foul_points + foul_points

    return {
        "score": score,
        "no_foul_points": no_foul_points,
        "foul_points": foul_points,
        "auto_points": auto_points,
        "teleop_points": teleop_points,
        "endgame_points": takeoff_points,
        "rp_1": rp_1,
        "rp_2": rp_2,
        "tiebreaker": tiebreaker,
        "comp_1": auto_mobility_points,
        "comp_2": auto_fuel_low,
        "comp_3": auto_fuel_high,
        "comp_4": auto_rotor_points,
        "comp_5": teleop_fuel_low,
        "comp_6": teleop_fuel_high,
        "comp_7": teleop_rotor_points,
        "comp_8": takeoff_points,
        "comp_9": 0,
        "comp_10": 0,
        "comp_11": 0,
        "comp_12": 0,
    }


def clean_breakdown_2018(
    key: str,
    breakdown: Dict[str, Any],
    score: int,
    no_foul_points: int,
    foul_points: int,
) -> BreakdownDict:
    auto_run_points = breakdown.get("autoRunPoints", 0)
    auto_switch_secs = breakdown.get("autoSwitchOwnershipSec", 0)
    auto_scale_secs = breakdown.get("autoScaleOwnershipSec", 0)

    teleop_switch_secs = breakdown.get("teleopSwitchOwnershipSec", 0) + +breakdown.get(
        "teleopSwitchBoostSec", 0
    )
    teleop_scale_secs = breakdown.get("teleopScaleOwnershipSec", 0) + breakdown.get(
        "teleopScaleBoostSec", 0
    )

    vault_points = breakdown.get("vaultPoints", 0)

    endgame_points = breakdown.get("endgamePoints", 0)

    rp_1 = bool(breakdown.get("faceTheBossRankingPoint", False))
    rp_2 = bool(breakdown.get("autoQuestRankingPoint", False))

    error = no_foul_points - (
        auto_run_points
        + 2 * auto_switch_secs
        + 2 * auto_scale_secs
        + teleop_switch_secs
        + teleop_scale_secs
        + vault_points
        + endgame_points
    )

    if error != 0:
        # increase the smaller, decrease the larger
        if error * teleop_switch_secs > error * teleop_scale_secs:
            teleop_scale_secs += error
        else:
            teleop_switch_secs += error

    auto_points = auto_run_points + 2 * auto_switch_secs + 2 * auto_scale_secs
    teleop_points = teleop_switch_secs + teleop_scale_secs + vault_points

    tiebreaker_points = endgame_points

    return {
        "score": score,
        "no_foul_points": no_foul_points,
        "foul_points": foul_points,
        "auto_points": auto_points,
        "teleop_points": teleop_points,
        "endgame_points": endgame_points,
        "rp_1": rp_1,
        "rp_2": rp_2,
        "tiebreaker": tiebreaker_points,
        "comp_1": auto_run_points,
        "comp_2": auto_switch_secs,
        "comp_3": auto_scale_secs,
        "comp_4": teleop_switch_secs,
        "comp_5": teleop_scale_secs,
        "comp_6": vault_points,
        "comp_7": endgame_points,
        "comp_8": 0,
        "comp_9": 0,
        "comp_10": 0,
        "comp_11": 0,
        "comp_12": 0,
    }


def count_pieces_2019(
    location: str, height: str, piece: str, breakdown: Dict[str, Any]
) -> int:
    if piece not in ["Panel", "Cargo"]:
        raise ValueError("Piece must be hatch or cargo")

    if location == "bay":
        if piece == "Panel":
            count = 0
            for i in range(1, 9):
                final = breakdown[f"bay{i}"]
                if "Panel" in final:
                    if i in [4, 5]:
                        count += 1
                    else:
                        start = breakdown[f"preMatchBay{i}"]
                        if "Panel" not in start and "Unknown" not in start:
                            count += 1
            return count
        elif piece == "Cargo":
            return sum(
                [1 if "Cargo" in breakdown[f"bay{i}"] else 0 for i in range(1, 9)]
            )
    elif location == "rocket":
        return sum(
            [
                1 if piece in breakdown[f"{height}{x}"] else 0
                for x in [
                    "LeftRocketFar",
                    "LeftRocketNear",
                    "RightRocketFar",
                    "RightRocketNear",
                ]
            ]
        )
    else:
        raise ValueError("Location must be bay or rocket")

    return 0


def clean_breakdown_2019(
    key: str,
    breakdown: Dict[str, Any],
    score: int,
    no_foul_points: int,
    foul_points: int,
) -> BreakdownDict:
    sandstorm_points = breakdown.get("sandStormBonusPoints", 0)

    bay_hatch = count_pieces_2019("bay", "any", "Panel", breakdown)
    bay_cargo = count_pieces_2019("bay", "any", "Cargo", breakdown)
    rocket_hatch_low = count_pieces_2019("rocket", "low", "Panel", breakdown)
    rocket_hatch_mid = count_pieces_2019("rocket", "mid", "Panel", breakdown)
    rocket_hatch_top = count_pieces_2019("rocket", "top", "Panel", breakdown)
    rocket_cargo_low = count_pieces_2019("rocket", "low", "Cargo", breakdown)
    rocket_cargo_mid = count_pieces_2019("rocket", "mid", "Cargo", breakdown)
    rocket_cargo_top = count_pieces_2019("rocket", "top", "Cargo", breakdown)

    hatch_points = 2 * (
        bay_hatch + rocket_hatch_low + rocket_hatch_mid + rocket_hatch_top
    )

    cargo_points = 3 * (
        bay_cargo + rocket_cargo_low + rocket_cargo_mid + rocket_cargo_top
    )

    hab_climb_points = breakdown.get("habClimbPoints", 0)

    rp_1 = bool(breakdown.get("habDockingRankingPoint", False))
    rp_2 = bool(breakdown.get("completeRocketRankingPoint", False))

    tiebreaker = cargo_points

    return {
        "score": score,
        "no_foul_points": no_foul_points,
        "foul_points": foul_points,
        "auto_points": sandstorm_points,
        "teleop_points": hatch_points + cargo_points,
        "endgame_points": hab_climb_points,
        "rp_1": rp_1,
        "rp_2": rp_2,
        "tiebreaker": tiebreaker,
        "comp_1": sandstorm_points,
        "comp_2": bay_hatch,
        "comp_3": bay_cargo,
        "comp_4": rocket_hatch_low,
        "comp_5": rocket_hatch_mid,
        "comp_6": rocket_hatch_top,
        "comp_7": rocket_cargo_low,
        "comp_8": rocket_cargo_mid,
        "comp_9": rocket_cargo_top,
        "comp_10": hab_climb_points,
        "comp_11": 0,
        "comp_12": 0,
    }


def clean_breakdown_2020(
    key: str,
    breakdown: Dict[str, Any],
    score: int,
    no_foul_points: int,
    foul_points: int,
) -> BreakdownDict:
    auto_init_line_points = breakdown.get("autoInitLinePoints", 0)

    auto_cells_bottom = breakdown.get("autoCellsBottom", 0)
    auto_cells_outer = breakdown.get("autoCellsOuter", 0)
    auto_cells_inner = breakdown.get("autoCellsInner", 0)

    auto_cell_points = (
        2 * auto_cells_bottom + 4 * auto_cells_outer + 6 * auto_cells_inner
    )

    teleop_cells_bottom = breakdown.get("teleopCellsBottom", 0)
    teleop_cells_outer = breakdown.get("teleopCellsOuter", 0)
    teleop_cells_inner = breakdown.get("teleopCellsInner", 0)

    teleop_cell_points = (
        teleop_cells_bottom + 2 * teleop_cells_outer + 3 * teleop_cells_inner
    )

    control_panel_points = breakdown.get("controlPanelPoints", 0)

    endgame_points = breakdown.get("endgamePoints", 0)

    rp_1 = bool(breakdown.get("shieldOperationalRankingPoint", False))
    rp_2 = bool(breakdown.get("shieldEnergizedRankingPoint", False))

    auto_points = auto_init_line_points + auto_cell_points
    teleop_points = teleop_cell_points + control_panel_points

    tiebreaker = auto_points

    return {
        "score": score,
        "no_foul_points": no_foul_points,
        "foul_points": foul_points,
        "auto_points": auto_points,
        "teleop_points": teleop_points,
        "endgame_points": endgame_points,
        "rp_1": rp_1,
        "rp_2": rp_2,
        "tiebreaker": tiebreaker,
        "comp_1": auto_init_line_points,
        "comp_2": auto_cells_bottom,
        "comp_3": auto_cells_outer,
        "comp_4": auto_cells_inner,
        "comp_5": teleop_cells_bottom,
        "comp_6": teleop_cells_outer,
        "comp_7": teleop_cells_inner,
        "comp_8": control_panel_points,
        "comp_9": endgame_points,
        "comp_10": 0,
        "comp_11": 0,
        "comp_12": 0,
    }


def clean_breakdown_2021(
    key: str,
    breakdown: Dict[str, Any],
    score: int,
    no_foul_points: int,
    foul_points: int,
) -> BreakdownDict:
    return clean_breakdown_2020(key, breakdown, score, no_foul_points, foul_points)


def clean_breakdown_2022(
    key: str,
    breakdown: Dict[str, Any],
    score: int,
    no_foul_points: int,
    foul_points: int,
) -> BreakdownDict:
    auto_taxi_points = breakdown.get("autoTaxiPoints", 0)

    auto_cargo_lower = (
        breakdown.get("autoCargoLowerBlue", 0)
        + breakdown.get("autoCargoLowerFar", 0)
        + breakdown.get("autoCargoLowerNear", 0)
        + breakdown.get("autoCargoLowerRed", 0)
    )
    auto_cargo_upper = (
        breakdown.get("autoCargoUpperBlue", 0)
        + breakdown.get("autoCargoUpperFar", 0)
        + breakdown.get("autoCargoUpperNear", 0)
        + breakdown.get("autoCargoUpperRed", 0)
    )

    # correct sensor issues
    initial_auto_cargo = 2 * auto_cargo_lower + 4 * auto_cargo_upper
    actual_auto_cargo_points = breakdown.get("autoCargoPoints", 0)
    auto_cargo_error = actual_auto_cargo_points - initial_auto_cargo
    if auto_cargo_error != 0:
        if auto_cargo_lower > auto_cargo_upper:
            auto_cargo_lower += auto_cargo_error / 2
        else:
            auto_cargo_upper += auto_cargo_error / 4

    auto_cargo_points = round(2 * auto_cargo_lower + 4 * auto_cargo_upper)
    auto_cargo_lower = round(auto_cargo_lower)
    auto_cargo_upper = round(auto_cargo_upper)

    teleop_cargo_lower = (
        breakdown.get("teleopCargoLowerBlue", 0)
        + breakdown.get("teleopCargoLowerFar", 0)
        + breakdown.get("teleopCargoLowerNear", 0)
        + breakdown.get("teleopCargoLowerRed", 0)
    )
    teleop_cargo_upper = (
        breakdown.get("teleopCargoUpperBlue", 0)
        + breakdown.get("teleopCargoUpperFar", 0)
        + breakdown.get("teleopCargoUpperNear", 0)
        + breakdown.get("teleopCargoUpperRed", 0)
    )

    # correct sensor issues
    initial_teleop_cargo = 1 * teleop_cargo_lower + 2 * teleop_cargo_upper
    actual_teleop_cargo_points = breakdown.get("teleopCargoPoints", 0)
    teleop_cargo_error = actual_teleop_cargo_points - initial_teleop_cargo
    if teleop_cargo_error != 0:
        if teleop_cargo_lower > teleop_cargo_upper:
            teleop_cargo_lower += teleop_cargo_error
        else:
            teleop_cargo_upper += teleop_cargo_error / 2

    teleop_cargo_points = round(teleop_cargo_lower + 2 * teleop_cargo_upper)
    teleop_cargo_lower = round(teleop_cargo_lower)
    teleop_cargo_upper = round(teleop_cargo_upper)

    endgame_points = breakdown.get("endgamePoints", 0)

    rp_1 = bool(breakdown.get("cargoBonusRankingPoint", False))
    rp_2 = bool(breakdown.get("hangarBonusRankingPoint", False))

    auto_points = auto_taxi_points + auto_cargo_points
    teleop_points = teleop_cargo_points

    tiebreaker = no_foul_points

    return {
        "score": score,
        "no_foul_points": no_foul_points,
        "foul_points": foul_points,
        "auto_points": auto_points,
        "teleop_points": teleop_points,
        "endgame_points": endgame_points,
        "rp_1": rp_1,
        "rp_2": rp_2,
        "tiebreaker": tiebreaker,
        "comp_1": auto_taxi_points,
        "comp_2": auto_cargo_lower,
        "comp_3": auto_cargo_upper,
        "comp_4": teleop_cargo_lower,
        "comp_5": teleop_cargo_upper,
        "comp_6": endgame_points,
        "comp_7": 0,
        "comp_8": 0,
        "comp_9": 0,
        "comp_10": 0,
        "comp_11": 0,
        "comp_12": 0,
    }


def count_pieces_2023(
    auto: List[str], teleop: List[str], piece: str, target: str
) -> int:
    if target == "auto":
        return len([x for x, y in zip(auto, teleop) if x == piece and y != "None"])
    elif target == "teleop":
        return len([x for x, y in zip(auto, teleop) if x == "None" and y == piece])
    else:
        raise ValueError("Target must be auto or teleop")


def clean_breakdown_2023(
    key: str,
    breakdown: Dict[str, Any],
    score: int,
    no_foul_points: int,
    foul_points: int,
) -> BreakdownDict:
    auto_mobility_points = breakdown.get("autoMobilityPoints", 0)

    auto_charge_station_points = breakdown.get("autoChargeStationPoints", 0)

    auto_com = breakdown.get("autoCommunity", {})
    teleop_com = breakdown.get("teleopCommunity", {})

    auto_b = auto_com.get("B", [])
    auto_m = auto_com.get("M", [])
    auto_t = auto_com.get("T", [])

    teleop_b = teleop_com.get("B", [])
    teleop_m = teleop_com.get("M", [])
    teleop_t = teleop_com.get("T", [])

    abcu = count_pieces_2023(auto_b, teleop_b, "Cube", "auto")
    abco = count_pieces_2023(auto_b, teleop_b, "Cone", "auto")
    amcu = count_pieces_2023(auto_m, teleop_m, "Cube", "auto")
    amco = count_pieces_2023(auto_m, teleop_m, "Cone", "auto")
    atcu = count_pieces_2023(auto_t, teleop_t, "Cube", "auto")
    atco = count_pieces_2023(auto_t, teleop_t, "Cone", "auto")
    auto_com_points = 3 * (abcu + abco) + 4 * (amcu + amco) + 6 * (atcu + atco)

    tbcu = count_pieces_2023(auto_b, teleop_b, "Cube", "teleop")
    tbco = count_pieces_2023(auto_b, teleop_b, "Cone", "teleop")
    tmcu = count_pieces_2023(auto_m, teleop_m, "Cube", "teleop")
    tmco = count_pieces_2023(auto_m, teleop_m, "Cone", "teleop")
    ttcu = count_pieces_2023(auto_t, teleop_t, "Cube", "teleop")
    ttco = count_pieces_2023(auto_t, teleop_t, "Cone", "teleop")

    sc = 0
    if breakdown.get("teleopGamePieceCount", 0) == 27:
        sc = breakdown.get("extraGamePieceCount", 0)

    teleop_com_points = 2 * (tbcu + tbco) + 3 * (tmcu + tmco + sc) + 5 * (ttcu + ttco)

    links = len(breakdown.get("links", []) or [])
    link_points = 5 * links

    endgame_charge_station_points = breakdown.get("endGameChargeStationPoints", 0)
    endgame_park_points = breakdown.get("endGameParkPoints", 0)

    rp_1 = bool(breakdown.get("sustainabilityBonusAchieved", False))
    rp_2 = bool(breakdown.get("activationBonusAchieved", False))

    auto_points = auto_charge_station_points + auto_com_points + auto_mobility_points
    teleop_points = teleop_com_points + link_points
    endgame_points = endgame_charge_station_points + endgame_park_points

    tiebreaker = no_foul_points

    return {
        "score": score,
        "no_foul_points": no_foul_points,
        "foul_points": foul_points,
        "auto_points": auto_points,
        "teleop_points": teleop_points,
        "endgame_points": endgame_points,
        "rp_1": rp_1,
        "rp_2": rp_2,
        "tiebreaker": tiebreaker,
        "comp_1": auto_mobility_points,
        "comp_2": auto_charge_station_points,
        "comp_3": abcu + tbcu,  # num bottom cubes (auto or teleop)
        "comp_4": abco + tbco,
        "comp_5": amcu + tmcu,
        "comp_6": amco + tmco,
        "comp_7": atcu + ttcu,
        "comp_8": atco + ttco,
        "comp_9": abcu + abco + amcu + amco + atcu + atco,  # total auto pieces
        "comp_10": link_points,
        "comp_11": endgame_charge_station_points,
        "comp_12": endgame_park_points,
    }


def clean_breakdown(
    key: str,
    year: int,
    offseason: bool,
    breakdown: Optional[Dict[str, Any]],
    score: Optional[int],
) -> BreakdownDict:
    out = empty_breakdown
    if breakdown is None or score is None or score == 0 or year < 2016:
        return out

    # Shared
    foul_points = breakdown.get("foulPoints", 0) + breakdown.get("adjustPoints", 0)
    no_foul_points = score - foul_points

    inputs = (key, breakdown, score, no_foul_points, foul_points)

    if year == 2016:
        out = clean_breakdown_2016(*inputs)
    elif year == 2017:
        out = clean_breakdown_2017(*inputs)
    elif year == 2018:
        out = clean_breakdown_2018(*inputs)
    elif year == 2019:
        out = clean_breakdown_2019(*inputs)
    elif year == 2020:
        out = clean_breakdown_2020(*inputs)
    elif year == 2021:
        out = clean_breakdown_2021(*inputs)
    elif year == 2022:
        out = clean_breakdown_2022(*inputs)
    elif year == 2023:
        out = clean_breakdown_2023(*inputs)
    else:
        out["no_foul_points"] = score

    if year >= 2016 and key not in INVALID_MATCH_KEYS:
        auto_points = out["auto_points"] or 0
        teleop_points = out["teleop_points"] or 0
        endgame_points = out["endgame_points"] or 0
        no_foul_points = out["no_foul_points"] or 0

        if not offseason:
            assert auto_points + teleop_points + endgame_points == no_foul_points

    return out
