from typing import Any, Dict, List, Optional, Tuple

from src.breakdown import all_keys
from src.tba.types import BreakdownDict, empty_breakdown

for year in range(2002, 2024):
    if len(all_keys[year]) > 25:
        # 7 standard (total, auto, teleop, endgame, rp_1, rp_2, tiebreaker) + 18 components
        raise ValueError(f"Too many keys for year {year}")
    all_keys[year] += ["empty"] * (23 - len(all_keys[year]))


def clean_breakdown_2016(
    key: str,
    alliance: str,
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

    if key == "2016mndu2_f1m2" and alliance == "blue":
        teleop_crossing_points += 15
        no_foul_points -= 10
        foul_points += 10

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

    if (key == "2016capl_f1m1" and alliance == "blue") or (
        key == "2016milsu_qf4m1" and alliance == "blue"
    ):
        rp_2 = False
        rp_2_points = 0

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
        "rp_3": None,
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
        "comp_12": None,
        "comp_13": None,
        "comp_14": None,
        "comp_15": None,
        "comp_16": None,
        "comp_17": None,
        "comp_18": None,
    }


def clean_breakdown_2017(
    key: str,
    alliance: str,
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

    kpa = auto_kpa_9ths // 9 + teleop_kpa_9ths // 9
    num_rotors = teleop_rotor_points // 40
    gears = (
        (1 if num_rotors >= 1 else 0)
        + (2 if num_rotors >= 2 else 0)
        + (4 if num_rotors >= 3 else 0)
        + (6 if num_rotors >= 4 else 0)
    )

    # Alliances often scored 3.x rotors, but truncated
    if num_rotors == 3:
        gears += 2

    rp_1 = bool(breakdown.get("rotorRankingPointAchieved", False))
    rp_2 = bool(breakdown.get("kPaRankingPointAchieved", False))

    rp_1_points = breakdown.get("rotorBonusPoints", 0)
    rp_2_points = breakdown.get("kPaBonusPoints", 0)

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
        "rp_3": None,
        "tiebreaker": tiebreaker,
        "comp_1": auto_mobility_points,
        "comp_2": auto_fuel_low,
        "comp_3": auto_fuel_high,
        "comp_4": auto_rotor_points,
        "comp_5": teleop_fuel_low,
        "comp_6": teleop_fuel_high,
        "comp_7": teleop_rotor_points,
        "comp_8": takeoff_points,
        "comp_9": kpa,
        "comp_10": gears,
        "comp_11": None,
        "comp_12": None,
        "comp_13": None,
        "comp_14": None,
        "comp_15": None,
        "comp_16": None,
        "comp_17": None,
        "comp_18": None,
    }


def clean_breakdown_2018(
    key: str,
    alliance: str,
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

    rp_1 = bool(breakdown.get("autoQuestRankingPoint", False))
    rp_2 = bool(breakdown.get("faceTheBossRankingPoint", False))

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
        "rp_3": None,
        "tiebreaker": tiebreaker_points,
        "comp_1": auto_run_points,
        "comp_2": auto_switch_secs,
        "comp_3": auto_scale_secs,
        "comp_4": teleop_switch_secs,
        "comp_5": teleop_scale_secs,
        "comp_6": vault_points,
        "comp_7": None,
        "comp_8": None,
        "comp_9": None,
        "comp_10": None,
        "comp_11": None,
        "comp_12": None,
        "comp_13": None,
        "comp_14": None,
        "comp_15": None,
        "comp_16": None,
        "comp_17": None,
        "comp_18": None,
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
    alliance: str,
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

    rocket = (
        rocket_hatch_low
        + rocket_hatch_mid
        + rocket_hatch_top
        + rocket_cargo_low
        + rocket_cargo_mid
        + rocket_cargo_top
    )

    pieces = bay_hatch + bay_cargo + rocket

    rp_1 = bool(breakdown.get("completeRocketRankingPoint", False))
    rp_2 = bool(breakdown.get("habDockingRankingPoint", False))

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
        "rp_3": None,
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
        "comp_11": rocket,
        "comp_12": pieces,
        "comp_13": None,
        "comp_14": None,
        "comp_15": None,
        "comp_16": None,
        "comp_17": None,
        "comp_18": None,
    }


def clean_breakdown_2020(
    key: str,
    alliance: str,
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

    cells = (
        auto_cells_bottom
        + auto_cells_outer
        + auto_cells_inner
        + teleop_cells_bottom
        + teleop_cells_outer
        + teleop_cells_inner
    )

    rp_1 = bool(breakdown.get("shieldEnergizedRankingPoint", False))
    rp_2 = bool(breakdown.get("shieldOperationalRankingPoint", False))

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
        "rp_3": None,
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
        "comp_10": cells,
        "comp_11": None,
        "comp_12": None,
        "comp_13": None,
        "comp_14": None,
        "comp_15": None,
        "comp_16": None,
        "comp_17": None,
        "comp_18": None,
    }


def clean_breakdown_2021(
    key: str,
    alliance: str,
    breakdown: Dict[str, Any],
    score: int,
    no_foul_points: int,
    foul_points: int,
) -> BreakdownDict:
    return clean_breakdown_2020(
        key, alliance, breakdown, score, no_foul_points, foul_points
    )


def clean_breakdown_2022(
    key: str,
    alliance: str,
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

    cargo = (
        auto_cargo_lower + auto_cargo_upper + teleop_cargo_lower + teleop_cargo_upper
    )

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
        "rp_3": None,
        "tiebreaker": tiebreaker,
        "comp_1": auto_taxi_points,
        "comp_2": auto_cargo_lower,
        "comp_3": auto_cargo_upper,
        "comp_4": teleop_cargo_lower,
        "comp_5": teleop_cargo_upper,
        "comp_6": endgame_points,
        "comp_7": cargo,
        "comp_8": None,
        "comp_9": None,
        "comp_10": None,
        "comp_11": None,
        "comp_12": None,
        "comp_13": None,
        "comp_14": None,
        "comp_15": None,
        "comp_16": None,
        "comp_17": None,
        "comp_18": None,
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
    alliance: str,
    breakdown: Dict[str, Any],
    score: int,
    no_foul_points: int,
    foul_points: int,
) -> BreakdownDict:
    auto_charge_station_points = breakdown.get("autoMobilityPoints", 0) + breakdown.get(
        "autoChargeStationPoints", 0
    )

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

    tbcu = count_pieces_2023(auto_b, teleop_b, "Cube", "teleop")
    tbco = count_pieces_2023(auto_b, teleop_b, "Cone", "teleop")
    tmcu = count_pieces_2023(auto_m, teleop_m, "Cube", "teleop")
    tmco = count_pieces_2023(auto_m, teleop_m, "Cone", "teleop")
    ttcu = count_pieces_2023(auto_t, teleop_t, "Cube", "teleop")
    ttco = count_pieces_2023(auto_t, teleop_t, "Cone", "teleop")

    sc = 0
    if breakdown.get("teleopGamePieceCount", 0) == 27:
        sc = breakdown.get("extraGamePieceCount", 0)

    auto_pieces = abcu + abco + amcu + amco + atcu + atco
    auto_grid_points = 3 * (abcu + abco) + 4 * (amcu + amco) + 6 * (atcu + atco)
    teleop_pieces = tbcu + tbco + tmcu + tmco + ttcu + ttco
    teleop_grid_points = 2 * (tbcu + tbco) + 3 * (tmcu + tmco + sc) + 5 * (ttcu + ttco)
    bottom_pieces = abcu + abco + tbcu + tbco
    middle_pieces = amcu + amco + tmcu + tmco
    top_pieces = atcu + atco + ttcu + ttco
    total_pieces = auto_pieces + teleop_pieces
    cubes_scored = abcu + amcu + atcu + tbcu + tmcu + ttcu
    cube_points = 3 * abcu + 4 * amcu + 6 * atcu + 2 * tbcu + 3 * tmcu + 5 * ttcu
    cones_scored = abco + amco + atco + tbco + tmco + ttco
    cone_points = 3 * abco + 4 * amco + 6 * atco + 2 * tbco + 3 * tmco + 5 * ttco
    grid_points = auto_grid_points + teleop_grid_points

    links = len(breakdown.get("links", []) or [])
    link_points = 5 * links

    endgame_charge_station_points = breakdown.get(
        "endGameChargeStationPoints", 0
    ) + breakdown.get("endGameParkPoints", 0)

    rp_1 = bool(breakdown.get("sustainabilityBonusAchieved", False))
    rp_2 = bool(breakdown.get("activationBonusAchieved", False))

    auto_points = auto_charge_station_points + auto_grid_points
    teleop_points = teleop_grid_points + link_points
    endgame_points = endgame_charge_station_points

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
        "rp_3": None,
        "tiebreaker": tiebreaker,
        "comp_1": auto_charge_station_points,
        "comp_2": auto_pieces,
        "comp_3": auto_grid_points,
        "comp_4": teleop_pieces,
        "comp_5": teleop_grid_points,
        "comp_6": bottom_pieces,
        "comp_7": middle_pieces,
        "comp_8": top_pieces,
        "comp_9": cubes_scored,
        "comp_10": cube_points,
        "comp_11": cones_scored,
        "comp_12": cone_points,
        "comp_13": total_pieces,
        "comp_14": links,
        "comp_15": grid_points,
        "comp_16": endgame_charge_station_points,
        "comp_17": None,
        "comp_18": None,
    }


def clean_breakdown_2024(
    key: str,
    alliance: str,
    breakdown: Dict[str, Any],
    score: int,
    no_foul_points: int,
    foul_points: int,
) -> BreakdownDict:
    # auto
    auto_leave_points = breakdown.get("autoLeavePoints", 0)
    auto_amp_notes = breakdown.get("autoAmpNoteCount", 0)
    auto_amp_note_points = 2 * auto_amp_notes
    auto_speaker_notes = breakdown.get("autoSpeakerNoteCount", 0)
    auto_speaker_note_points = 5 * auto_speaker_notes
    auto_notes = auto_amp_notes + auto_speaker_notes
    auto_note_points = auto_amp_note_points + auto_speaker_note_points
    auto_points = auto_leave_points + auto_note_points

    # teleop
    teleop_amp_notes = breakdown.get("teleopAmpNoteCount", 0)
    teleop_amp_note_points = 1 * teleop_amp_notes
    teleop_speaker_notes = breakdown.get("teleopSpeakerNoteCount", 0)
    teleop_speaker_amplified_notes = breakdown.get("teleopSpeakerNoteAmplifiedCount", 0)
    # count both unamplified and amplified notes
    teleop_speaker_notes += teleop_speaker_amplified_notes
    teleop_speaker_points = (
        2 * teleop_speaker_notes + 3 * teleop_speaker_amplified_notes
    )
    teleop_notes = teleop_amp_notes + teleop_speaker_notes
    teleop_note_points = teleop_amp_note_points + teleop_speaker_points
    teleop_points = teleop_note_points

    # combined
    amp_notes = auto_amp_notes + teleop_amp_notes
    amp_points = auto_amp_note_points + teleop_amp_note_points
    speaker_notes = auto_speaker_notes + teleop_speaker_notes
    speaker_points = auto_speaker_note_points + teleop_speaker_points
    amplified_notes = teleop_speaker_amplified_notes
    total_notes = auto_notes + teleop_notes
    total_note_points = auto_note_points + teleop_note_points

    # endgame
    endgame_park_points = breakdown.get("endGameParkPoints", 0)
    endgame_on_stage_points = breakdown.get("endGameOnStagePoints", 0)
    endgame_harmony_points = breakdown.get("endGameHarmonyPoints", 0)
    endgame_trap_points = breakdown.get("endGameNoteInTrapPoints", 0)
    endgame_spotlight_points = breakdown.get("endGameSpotLightBonusPoints", 0)
    endgame_points = (
        endgame_park_points
        + endgame_on_stage_points
        + endgame_harmony_points
        + endgame_trap_points
        + endgame_spotlight_points
    )

    # other
    rp_1 = bool(breakdown.get("melodyBonusAchieved", False))
    rp_2 = bool(breakdown.get("ensembleBonusAchieved", False))
    tiebreaker = int(breakdown.get("coopertitionBonusAchieved", False))

    return {
        "score": score,
        "no_foul_points": no_foul_points,
        "foul_points": foul_points,
        "auto_points": auto_points,
        "teleop_points": teleop_points,
        "endgame_points": endgame_points,
        "rp_1": rp_1,
        "rp_2": rp_2,
        "rp_3": None,
        "tiebreaker": tiebreaker,
        "comp_1": auto_leave_points,
        "comp_2": auto_notes,
        "comp_3": auto_note_points,
        "comp_4": teleop_notes,
        "comp_5": teleop_note_points,
        "comp_6": amp_notes,
        "comp_7": amp_points,
        "comp_8": speaker_notes,
        "comp_9": speaker_points,
        "comp_10": amplified_notes,
        "comp_11": total_notes,
        "comp_12": total_note_points,
        "comp_13": endgame_park_points,
        "comp_14": endgame_on_stage_points,
        "comp_15": endgame_harmony_points,
        "comp_16": endgame_trap_points,
        "comp_17": endgame_spotlight_points,
        "comp_18": None,
    }


def clean_breakdown_2025(
    key: str,
    alliance: str,
    breakdown: Dict[str, Any],
    score: int,
    no_foul_points: int,
    foul_points: int,
) -> BreakdownDict:
    # auto
    auto_leave_points = breakdown.get("autoMobilityPoints", 0)
    auto_coral = breakdown.get("autoCoralCount", 0)
    auto_coral_points = breakdown.get("autoCoralPoints", 0)
    auto_reef: Dict[str, int] = breakdown.get("autoReef", {})
    auto_top_coral = auto_reef.get("tba_topRowCount", 0)
    auto_mid_coral = auto_reef.get("tba_midRowCount", 0)
    auto_bot_coral = auto_reef.get("tba_botRowCount", 0)
    auto_trough_coral = auto_reef.get("trough", 0)
    auto_points = auto_leave_points + auto_coral_points

    # teleop
    teleop_coral = breakdown.get("teleopCoralCount", 0)
    teleop_coral_points = breakdown.get("teleopCoralPoints", 0)
    teleop_reef: Dict[str, int] = breakdown.get("teleopReef", {})
    # the counts are as of end of teleop, subtract auto to get teleop contribution
    teleop_top_coral = teleop_reef.get("tba_topRowCount", 0) - auto_top_coral
    teleop_mid_coral = teleop_reef.get("tba_midRowCount", 0) - auto_mid_coral
    teleop_bot_coral = teleop_reef.get("tba_botRowCount", 0) - auto_bot_coral
    teleop_trough_coral = teleop_reef.get("trough", 0)
    processor_algae = breakdown.get("wallAlgaeCount", 0)
    processor_algae_points = 6 * processor_algae
    net_algae = breakdown.get("netAlgaeCount", 0)
    net_algae_points = 4 * net_algae
    total_algae_points = processor_algae_points + net_algae_points
    teleop_points = teleop_coral_points + total_algae_points

    # combined
    coral_l1 = auto_trough_coral + teleop_trough_coral
    coral_l2 = auto_bot_coral + teleop_bot_coral
    coral_l3 = auto_mid_coral + teleop_mid_coral
    coral_l4 = auto_top_coral + teleop_top_coral
    total_coral_points = auto_coral_points + teleop_coral_points
    total_game_pieces = (
        coral_l1 + coral_l2 + coral_l3 + coral_l4 + net_algae + processor_algae
    )

    # endgame
    barge_points = breakdown.get("endGameBargePoints", 0)
    endgame_points = barge_points

    # other
    auto_rp = bool(breakdown.get("autoBonusAchieved", False))
    coral_rp = bool(breakdown.get("coralBonusAchieved", False))
    barge_rp = bool(breakdown.get("bargeBonusAchieved", False))
    tiebreaker_points = int(breakdown.get("coopertitionCriteriaMet", False))

    return {
        "score": score,
        "no_foul_points": no_foul_points,
        "foul_points": foul_points,
        "auto_points": auto_points,
        "teleop_points": teleop_points,
        "endgame_points": endgame_points,
        "rp_1": auto_rp,
        "rp_2": coral_rp,
        "rp_3": barge_rp,
        "tiebreaker": tiebreaker_points,
        "comp_1": auto_leave_points,
        "comp_2": auto_coral,
        "comp_3": auto_coral_points,
        "comp_4": teleop_coral,
        "comp_5": teleop_coral_points,
        "comp_6": coral_l1,
        "comp_7": coral_l2,
        "comp_8": coral_l3,
        "comp_9": coral_l4,
        "comp_10": total_coral_points,
        "comp_11": processor_algae,
        "comp_12": processor_algae_points,
        "comp_13": net_algae,
        "comp_14": net_algae_points,
        "comp_15": total_algae_points,
        "comp_16": total_game_pieces,
        "comp_17": barge_points,
        "comp_18": None,
    }


def clean_breakdown(
    key: str,
    alliance: str,
    year: int,
    breakdown: Optional[Dict[str, Any]],
    score: Optional[int],
) -> BreakdownDict:
    out = empty_breakdown
    if breakdown is None or score is None or score == 0 or year < 2016:
        return out

    # Shared
    foul_points = breakdown.get("foulPoints", 0) + breakdown.get("adjustPoints", 0)
    no_foul_points = score - foul_points

    inputs = (
        key,
        alliance,
        breakdown,
        score,
        no_foul_points,
        foul_points,
    )

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
    elif year == 2024:
        out = clean_breakdown_2024(*inputs)
    elif year == 2025:
        out = clean_breakdown_2025(*inputs)
    else:
        out["no_foul_points"] = score

    if year >= 2016:
        auto_points = out["auto_points"] or 0
        teleop_points = out["teleop_points"] or 0
        endgame_points = out["endgame_points"] or 0
        no_foul_points = out["no_foul_points"] or 0

        error = no_foul_points - (auto_points + teleop_points + endgame_points)
        if error != 0:
            out["teleop_points"] = (out["teleop_points"] or 0) + error
            print("ERROR", key, alliance, error)

    return out


def post_clean_breakdown(
    key: str, year: int, red_breakdown: BreakdownDict, blue_breakdown: BreakdownDict
) -> Tuple[BreakdownDict, BreakdownDict]:
    if year == 2018:
        # "comp_1": auto_run_points,
        # "comp_2": auto_switch_secs,
        # "comp_3": auto_scale_secs,
        # "comp_4": teleop_switch_secs,
        # "comp_5": teleop_scale_secs,
        # "comp_6": vault_points,
        # "comp_7": auto_scale_power,
        # "comp_8": switch_power,
        # "comp_9": scale_power,
        # "comp_10": opp_switch_power,
        red_auto_scale_secs = red_breakdown["comp_3"] or 0
        blue_auto_scale_secs = blue_breakdown["comp_3"] or 0
        red_switch_secs = red_breakdown["comp_4"] or 0
        blue_switch_secs = blue_breakdown["comp_4"] or 0
        red_scale_secs = red_breakdown["comp_5"] or 0
        blue_scale_secs = blue_breakdown["comp_5"] or 0
        red_opp_switch_secs = 145 - (blue_breakdown["comp_4"] or 0)
        blue_opp_switch_secs = 145 - (red_breakdown["comp_4"] or 0)

        red_breakdown["comp_7"] = min(
            1, max(0, (15 + red_auto_scale_secs - blue_auto_scale_secs) / 30)
        )
        blue_breakdown["comp_7"] = min(
            1, max(0, (15 + blue_auto_scale_secs - red_auto_scale_secs) / 30)
        )

        red_breakdown["comp_8"] = min(1, red_switch_secs / 145)
        blue_breakdown["comp_8"] = min(1, blue_switch_secs / 145)

        red_breakdown["comp_9"] = min(
            1, max(0, (145 + red_scale_secs - blue_scale_secs) / 290)
        )
        blue_breakdown["comp_9"] = min(
            1, max(0, (145 + blue_scale_secs - red_scale_secs) / 290)
        )

        red_breakdown["comp_10"] = min(1, red_opp_switch_secs / 145)
        blue_breakdown["comp_10"] = min(1, blue_opp_switch_secs / 145)

    if year == 2025:
        # tiebreaker is not set correctly in the API so we compute it manually
        # requires at least two processor algae (comp_11) per alliance
        red_processor_algae = red_breakdown["comp_11"] or 0
        blue_processor_algae = blue_breakdown["comp_11"] or 0
        coopertition = min(red_processor_algae, blue_processor_algae) >= 2
        red_breakdown["tiebreaker"] = int(coopertition)
        blue_breakdown["tiebreaker"] = int(coopertition)

    return red_breakdown, blue_breakdown
