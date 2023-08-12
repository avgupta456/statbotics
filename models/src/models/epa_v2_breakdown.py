from collections import defaultdict
from typing import Any, Dict, List, Tuple

from src.models.epa_v2_math import t_prob_gt_0, zero_sigmoid, unit_sigmoid

import numpy as np

# Always put total_points first
all_keys: Dict[int, List[str]] = defaultdict(lambda: ["no_foul_points", "foul_points"])
all_keys[2016] = [
    "no_foul_points",
    "foul_points",
    "auto_reach_points",
    "auto_crossing_points",
    "auto_low_boulders",
    "auto_high_boulders",
    "teleop_crossing_points",
    "teleop_low_boulders",
    "teleop_high_boulders",
    "challenge_points",
    "scale_points",
    # computed
    "defenses",
    "boulders",
    "rp_2_power",
    "auto_points",
    "teleop_points",
    "endgame_points",
]
all_keys[2017] = [
    "no_foul_points",
    "foul_points",
    "auto_mobility_points",
    "auto_fuel_low",
    "auto_fuel_high",
    "auto_rotor_points",
    "teleop_fuel_low",
    "teleop_fuel_high",
    "teleop_rotor_points",
    "takeoff_points",
    # computed
    "kpa",
    "gears",
    "auto_points",
    "teleop_points",
    "endgame_points",
]
all_keys[2018] = [
    "no_foul_points",
    "foul_points",
    "auto_run_points",
    "auto_switch_secs",
    "auto_scale_secs",
    "teleop_switch_secs",
    "teleop_scale_secs",
    "vault_points",
    "endgame_points",
    # computed
    "switch_power",
    "scale_power",
    "opp_switch_power",
    "rp_1_power",
    "rp_2_power",
    "auto_points",
    "teleop_points",
    "endgame_points",
]
all_keys[2019] = [
    "no_foul_points",
    "foul_points",
    "sandstorm_points",
    "bay_hatch",
    "bay_cargo",
    "rocket_hatch_low",
    "rocket_hatch_mid",
    "rocket_hatch_top",
    "rocket_cargo_low",
    "rocket_cargo_mid",
    "rocket_cargo_top",
    "hab_climb_points",
    # computed
    "rocket_mid_top",
    "hatch",
    "cargo",
    "auto_points",
    "teleop_points",
    "endgame_points",
]
all_keys[2020] = [
    "no_foul_points",
    "foul_points",
    "auto_init_line_points",
    "auto_cells_bottom",
    "auto_cells_outer",
    "auto_cells_inner",
    "teleop_cells_bottom",
    "teleop_cells_outer",
    "teleop_cells_inner",
    "control_panel_points",
    "endgame_points",
    # computed
    "cells",
    "auto_points",
    "teleop_points",
    "endgame_points",
]
all_keys[2022] = [
    "no_foul_points",
    "foul_points",
    "auto_taxi_points",
    "auto_cargo_lower",
    "auto_cargo_upper",
    "teleop_cargo_lower",
    "teleop_cargo_upper",
    "endgame_points",
    # computed
    "cargo",
    "auto_points",
    "teleop_points",
    "endgame_points",
]
all_keys[2023] = [
    "no_foul_points",
    "foul_points",
    "auto_mobility_points",
    "auto_charge_station_points",
    "auto_low_cubes",
    "auto_low_cones",
    "auto_mid_cubes",
    "auto_mid_cones",
    "auto_high_cubes",
    "auto_high_cones",
    "teleop_low_cubes",
    "teleop_low_cones",
    "teleop_mid_cubes",
    "teleop_mid_cones",
    "teleop_high_cubes",
    "teleop_high_cones",
    "links",
    "endgame_charge_station_points",
    "endgame_park_points",
    # computed
    "charge_station_points",
    "auto_points",
    "teleop_points",
    "endgame_points",
]


all_headers: Dict[int, str] = defaultdict(lambda: "Team\tLow\tMean\tHigh")
all_headers[2016] = "Team\tAReach\tACross\tALow\tAHigh\tTCross\tTLow\tTHigh\tTChal\tTScale\tDef\tBoulder\tRP2Pow\tAuto\tTeleop\tEndgame\tLow\tMean\tHigh"  # type: ignore
all_headers[2017] = "Team\tAutoMob\tALow\tAHigh\tAutoRot\tTLow\tTHigh\tTeleRot\tTakeoff\tkPA\tGears\tAuto\tTeleop\tEndgame\tLow\tMean\tHigh"  # type: ignore
all_headers[2018] = "Team\tAutoRun\tASwitch\tAScale\tTSwitch\tTScale\tVault\tEnd\tSwPow\tScPow\tOSwPow\tRP1Pow\tRP2Pow\tAuto\tTeleop\tEndgame\tLow\tMean\tHigh"  # type: ignore
all_headers[2019] = "Team\tSS\tBHatch\tBCargo\tRHatchL\tRHatchM\tRHatchT\tRCargoL\tRCargoM\tRCargoT\tHClimb\tMidTop\tHatch\tCargo\tAuto\tTeleop\tEndgame\tLow\tMean\tHigh"  # type: ignore
all_headers[2020] = "Team\tInit\tABot\tAOuter\tAInner\tTBot\tTOuter\tTInner\tCP\tEnd\tCells\tAuto\tTeleop\tEndgame\tLow\tMean\tHigh"  # type: ignore
all_headers[2022] = "Team\tTaxi\tALow\tAHigh\tTLow\tTHigh\tEndgame\tCargo\tAuto\tTeleop\tEndgame\tLow\tMean\tHigh"  # type: ignore
all_headers[2023] = "Team\tMob\tAuto CS\tALCu\tALCo\tAMCu\tAMCo\tAHCu\tAHCo\tTLCu\tTLCo\tTMCu\tTMCo\tTHCu\tTHCo\tLinks\tEnd CS\tPark\tAll CS\tAuto\tTeleop\tEndgame\tLow\tMean\tHigh"  # type: ignore


def expand_breakdown(
    year: int,
    breakdown: Dict[str, int | float],
    opp_breakdown: Dict[str, int | float],
    mean: bool = False,
) -> Any:
    # mean flag denotes if individual breakdown or week 1 mean
    if year == 2016:
        breakdown["defenses"] = (
            breakdown["auto_crossing_points"] / 10
            + breakdown["teleop_crossing_points"] / 5
        )

        breakdown["boulders"] = (
            breakdown["auto_low_boulders"]
            + breakdown["auto_high_boulders"]
            + breakdown["teleop_low_boulders"]
            + breakdown["teleop_high_boulders"]
        )

        num_robots = breakdown["challenge_points"] / 5 + breakdown["scale_points"] / 15
        breakdown["rp_2_power"] = 0.5 if mean else num_robots > 2.5

        breakdown["auto_points"] = (
            breakdown["auto_reach_points"]
            + breakdown["auto_crossing_points"]
            + 5 * breakdown["auto_low_boulders"]
            + 10 * breakdown["auto_high_boulders"]
        )

        breakdown["teleop_points"] = (
            breakdown["teleop_crossing_points"]
            + 2 * breakdown["teleop_low_boulders"]
            + 5 * breakdown["teleop_high_boulders"]
        )

        breakdown["endgame_points"] = (
            breakdown["challenge_points"] + breakdown["scale_points"]
        )

    elif year == 2017:
        breakdown["kpa"] = (
            breakdown["auto_fuel_low"] / 3
            + breakdown["auto_fuel_high"]
            + breakdown["teleop_fuel_low"] / 9
            + breakdown["teleop_fuel_high"] / 3
        )

        num_rotors = breakdown["teleop_rotor_points"] // 40
        num_gears = (
            (1 if num_rotors >= 1 else 0)
            + (2 if num_rotors >= 2 else 0)
            + (4 if num_rotors >= 3 else 0)
            + (6 if num_rotors >= 4 else 0)
        )

        # Alliances often scored 3.x rotors, but truncated
        if num_rotors == 3:
            num_gears += 2

        breakdown["gears"] = num_gears

        breakdown["auto_points"] = (
            breakdown["auto_mobility_points"]
            + breakdown["auto_fuel_low"] / 3
            + breakdown["auto_fuel_high"]
            + breakdown["auto_rotor_points"]
        )

        breakdown["teleop_points"] = (
            breakdown["teleop_fuel_low"] / 9
            + breakdown["teleop_fuel_high"] / 3
            + breakdown["teleop_rotor_points"]
        )

        breakdown["endgame_points"] = breakdown["takeoff_points"]

    elif year == 2018:
        my_switch_secs = breakdown["teleop_switch_secs"]
        my_scale_secs = breakdown["teleop_scale_secs"]
        my_opp_switch_secs = 145 - opp_breakdown["teleop_switch_secs"]

        opp_scale_secs = opp_breakdown["teleop_scale_secs"]
        total_scale_secs = max(1, my_scale_secs + opp_scale_secs)

        breakdown["switch_power"] = min(1, my_switch_secs / 145)
        breakdown["scale_power"] = min(1, my_scale_secs / total_scale_secs)
        breakdown["opp_switch_power"] = min(1, my_opp_switch_secs / 145)

        breakdown["rp_1_power"] = breakdown["rp_1"]
        breakdown["rp_2_power"] = breakdown["rp_2"]

        breakdown["auto_points"] = (
            breakdown["auto_run_points"]
            + 2 * breakdown["auto_switch_secs"]
            + 2 * breakdown["auto_scale_secs"]
        )

        breakdown["teleop_points"] = (
            breakdown["teleop_switch_secs"]
            + breakdown["teleop_scale_secs"]
            + breakdown["vault_points"]
        )

        breakdown["endgame_points"] = breakdown["endgame_points"]

    elif year == 2019:
        breakdown["rocket_mid_top"] = (
            breakdown["rocket_hatch_mid"]
            + breakdown["rocket_cargo_mid"]
            + breakdown["rocket_hatch_top"]
            + breakdown["rocket_cargo_top"]
        )

        breakdown["hatch"] = (
            breakdown["bay_hatch"]
            + breakdown["rocket_hatch_low"]
            + breakdown["rocket_hatch_mid"]
            + breakdown["rocket_hatch_top"]
        )

        breakdown["cargo"] = (
            breakdown["bay_cargo"]
            + breakdown["rocket_cargo_low"]
            + breakdown["rocket_cargo_mid"]
            + breakdown["rocket_cargo_top"]
        )

        breakdown["auto_points"] = breakdown["sandstorm_points"]

        breakdown["teleop_points"] = (
            2 * breakdown["bay_hatch"]
            + 3 * breakdown["bay_cargo"]
            + 2 * breakdown["rocket_hatch_low"]
            + 2 * breakdown["rocket_hatch_mid"]
            + 2 * breakdown["rocket_hatch_top"]
            + 3 * breakdown["rocket_cargo_low"]
            + 3 * breakdown["rocket_cargo_mid"]
            + 3 * breakdown["rocket_cargo_top"]
        )

        breakdown["endgame_points"] = breakdown["hab_climb_points"]

    elif year == 2020:
        breakdown["cells"] = (
            breakdown["auto_cells_bottom"]
            + breakdown["auto_cells_outer"]
            + breakdown["auto_cells_inner"]
            + breakdown["teleop_cells_bottom"]
            + breakdown["teleop_cells_outer"]
            + breakdown["teleop_cells_inner"]
        )

        breakdown["auto_points"] = (
            breakdown["auto_init_line_points"]
            + 2 * breakdown["auto_cells_bottom"]
            + 4 * breakdown["auto_cells_outer"]
            + 6 * breakdown["auto_cells_inner"]
        )

        breakdown["teleop_points"] = (
            breakdown["teleop_cells_bottom"]
            + 2 * breakdown["teleop_cells_outer"]
            + 3 * breakdown["teleop_cells_inner"]
        )

    elif year == 2022:
        breakdown["cargo"] = (
            breakdown["auto_cargo_lower"]
            + breakdown["auto_cargo_upper"]
            + breakdown["teleop_cargo_lower"]
            + breakdown["teleop_cargo_upper"]
        )

        breakdown["auto_points"] = (
            breakdown["auto_taxi_points"]
            + 2 * breakdown["auto_cargo_lower"]
            + 4 * breakdown["auto_cargo_upper"]
        )

        breakdown["teleop_points"] = (
            1 * breakdown["teleop_cargo_lower"] + 2 * breakdown["teleop_cargo_upper"]
        )

    elif year == 2023:
        breakdown["charge_station_points"] = (
            breakdown["auto_charge_station_points"]
            + breakdown["endgame_charge_station_points"]
        )

        breakdown["auto_points"] = (
            breakdown["auto_mobility_points"]
            + breakdown["auto_charge_station_points"]
            + 3 * breakdown["auto_low_cubes"]
            + 3 * breakdown["auto_low_cones"]
            + 4 * breakdown["auto_mid_cubes"]
            + 4 * breakdown["auto_mid_cones"]
            + 6 * breakdown["auto_high_cubes"]
            + 6 * breakdown["auto_high_cones"]
        )

        breakdown["teleop_points"] = (
            2 * breakdown["teleop_low_cubes"]
            + 2 * breakdown["teleop_low_cones"]
            + 3 * breakdown["teleop_mid_cubes"]
            + 3 * breakdown["teleop_mid_cones"]
            + 5 * breakdown["teleop_high_cubes"]
            + 5 * breakdown["teleop_high_cones"]
            + 5 * breakdown["links"]
        )

        breakdown["endgame_points"] = (
            breakdown["endgame_charge_station_points"]
            + breakdown["endgame_park_points"]
        )

    return np.array([breakdown[k] for k in all_keys[year]])


def post_process_breakdown(
    year: int, key: str, breakdown: Any, opp_breakdown: Any
) -> Any:
    # Updates breakdown for both score prediction and EPA update

    keys = all_keys[year]
    total_change = 0

    if year == 2016:
        rp_2_power = breakdown[keys.index("rp_2_power")]
        new_rp_2_power = unit_sigmoid(rp_2_power)

        breakdown[keys.index("rp_2_power")] = new_rp_2_power

    elif year == 2018:
        my_switch_power = breakdown[keys.index("switch_power")]
        opp_opp_switch_power = opp_breakdown[keys.index("opp_switch_power")]
        new_switch_power = zero_sigmoid(my_switch_power - opp_opp_switch_power)

        my_scale_power = breakdown[keys.index("scale_power")]
        opp_scale_power = opp_breakdown[keys.index("scale_power")]
        new_scale_power = zero_sigmoid(my_scale_power - opp_scale_power)

        my_opp_switch_power = breakdown[keys.index("opp_switch_power")]
        opp_switch_power = opp_breakdown[keys.index("switch_power")]
        new_opp_switch_power = zero_sigmoid(my_opp_switch_power - opp_switch_power)

        rp_1_power = breakdown[keys.index("rp_1_power")]
        new_rp_1_power = unit_sigmoid(rp_1_power)

        rp_2_power = breakdown[keys.index("rp_2_power")]
        new_rp_2_power = unit_sigmoid(rp_2_power)

        breakdown[keys.index("switch_power")] = new_switch_power
        breakdown[keys.index("scale_power")] = new_scale_power
        breakdown[keys.index("opp_switch_power")] = new_opp_switch_power
        breakdown[keys.index("rp_1_power")] = new_rp_1_power
        breakdown[keys.index("rp_2_power")] = new_rp_2_power

    elif year == 2023:
        # ahcui = Auto High CUbes Index, etc
        ahcui = keys.index("auto_high_cubes")
        ahcoi = keys.index("auto_high_cones")
        thcui = keys.index("teleop_high_cubes")
        thcoi = keys.index("teleop_high_cones")
        amcui = keys.index("auto_mid_cubes")
        amcoi = keys.index("auto_mid_cones")
        tmcui = keys.index("teleop_mid_cubes")
        tmcoi = keys.index("teleop_mid_cones")
        alcui = keys.index("auto_low_cubes")
        alcoi = keys.index("auto_low_cones")
        tlcui = keys.index("teleop_low_cubes")
        tlcoi = keys.index("teleop_low_cones")

        auto_high = breakdown[ahcui] + breakdown[ahcoi]
        teleop_high = breakdown[thcui] + breakdown[thcoi]
        total_high = auto_high + teleop_high

        if total_high > 9:
            teleop_mid = breakdown[tmcui] + breakdown[tmcoi]
            extra_high = total_high - 9
            breakdown[thcui] *= (9 - auto_high) / teleop_high
            breakdown[thcoi] *= (9 - auto_high) / teleop_high
            breakdown[tmcui] *= (teleop_mid + extra_high) / teleop_mid
            breakdown[tmcoi] *= (teleop_mid + extra_high) / teleop_mid

            # each game piece moving from high to mid is 2 points lost
            total_change -= extra_high * 2

        auto_mid = breakdown[amcui] + breakdown[amcoi]
        teleop_mid = breakdown[tmcui] + breakdown[tmcoi]
        total_mid = auto_mid + teleop_mid
        if total_mid > 9:
            teleop_low = breakdown[tlcui] + breakdown[tlcoi]
            extra_mid = total_mid - 9
            breakdown[tmcui] *= (9 - auto_mid) / teleop_mid
            breakdown[tmcoi] *= (9 - auto_mid) / teleop_mid
            breakdown[tlcui] *= (teleop_low + extra_mid) / teleop_low
            breakdown[tlcoi] *= (teleop_low + extra_mid) / teleop_low

            # each game piece moving from mid to low is 1 point lost
            total_change -= extra_mid

        auto_low = breakdown[alcui] + breakdown[alcoi]
        teleop_low = breakdown[tlcui] + breakdown[tlcoi]
        total_low = auto_low + teleop_low
        if total_low > 9 and total_mid > 9 and total_high > 9:
            extra_low = total_low - 9
            breakdown[tlcui] *= (9 - auto_low) / teleop_low
            breakdown[tlcoi] *= (9 - auto_low) / teleop_low
            # supercharge counts as mid cubes
            breakdown[tmcui] += extra_low
            # each game piece moving from low to supercharge is 1 point gained
            total_change += extra_low

    breakdown[0] += total_change

    return breakdown


def get_pred_rps(
    year: int, week: int, breakdown_mean: Any, breakdown_sd: Any
) -> Tuple[float, float]:
    DISCOUNT = 0.85  # Teams try harder when near the threshold

    keys = all_keys[year]

    rp_1, rp_2 = 0, 0

    if year == 2016:
        defenses_mean = breakdown_mean[keys.index("defenses")]
        defenses_sd = breakdown_sd[keys.index("defenses")]

        boulders_mean = breakdown_mean[keys.index("boulders")]
        boulders_sd = breakdown_sd[keys.index("boulders")]

        rp_1 = t_prob_gt_0(defenses_mean - 8 * DISCOUNT, defenses_sd)

        # rp_2_power only captures if three robots challenge
        rp_2 = breakdown_mean[keys.index("rp_2_power")]
        if week < 8:
            rp_2 *= t_prob_gt_0(boulders_mean - 8 * DISCOUNT, boulders_sd)
        else:
            rp_2 *= t_prob_gt_0(boulders_mean - 10 * DISCOUNT, boulders_sd)

    elif year == 2017:
        kpa_mean = breakdown_mean[keys.index("kpa")]
        kpa_sd = breakdown_sd[keys.index("kpa")]

        gears_mean = breakdown_mean[keys.index("gears")]
        gears_sd = breakdown_sd[keys.index("gears")]

        rp_1 = t_prob_gt_0(kpa_mean - 40 * DISCOUNT, kpa_sd)
        rp_2 = t_prob_gt_0(gears_mean - 13 * DISCOUNT, gears_sd)

    elif year == 2018:
        rp_1 = breakdown_mean[keys.index("rp_1_power")]
        rp_2 = breakdown_mean[keys.index("rp_2_power")]

    elif year == 2019:
        hab_points_mean = breakdown_mean[keys.index("hab_climb_points")]
        hab_points_sd = breakdown_sd[keys.index("hab_climb_points")]

        rocket_mid_top_mean = breakdown_mean[keys.index("rocket_mid_top")]
        rocket_mid_top_sd = breakdown_sd[keys.index("rocket_mid_top")]

        rp_1 = t_prob_gt_0(hab_points_mean - 15 * DISCOUNT, hab_points_sd)

        # assume bottom is easy, top is attempted less since no incentive
        rp_2 = t_prob_gt_0(rocket_mid_top_mean - 8 * DISCOUNT, rocket_mid_top_sd)

    elif year == 2020:
        endgame_points_mean = breakdown_mean[keys.index("endgame_points")]
        endgame_points_sd = breakdown_sd[keys.index("endgame_points")]

        cells_mean = breakdown_mean[keys.index("cells")]
        cells_sd = breakdown_sd[keys.index("cells")]

        rp_1 = t_prob_gt_0(endgame_points_mean - 65 * DISCOUNT, cells_sd)
        rp_2 = t_prob_gt_0(cells_mean - 49 * DISCOUNT, endgame_points_sd)

    elif year == 2022:
        cargo_mean = breakdown_mean[keys.index("cargo")]
        cargo_sd = breakdown_sd[keys.index("cargo")]

        endgame_points_mean = breakdown_mean[keys.index("endgame_points")]
        endgame_points_sd = breakdown_sd[keys.index("endgame_points")]

        rp_1 = t_prob_gt_0(cargo_mean - 20 * DISCOUNT, cargo_sd)
        rp_2 = t_prob_gt_0(endgame_points_mean - 16 * DISCOUNT, endgame_points_sd)

    elif year == 2023:
        links_mean = breakdown_mean[keys.index("links")]
        links_sd = breakdown_sd[keys.index("links")]

        charge_station_points_mean = breakdown_mean[keys.index("charge_station_points")]
        charge_station_points_sd = breakdown_sd[keys.index("charge_station_points")]

        if week < 8:
            rp_1 = t_prob_gt_0(links_mean - 4 * DISCOUNT, links_sd)
        else:
            rp_1 = t_prob_gt_0(links_mean - 5 * DISCOUNT, links_sd)

        rp_2 = t_prob_gt_0(
            charge_station_points_mean - 26 * DISCOUNT, charge_station_points_sd
        )

    return rp_1, rp_2


def get_score_from_breakdown(
    year: int,
    breakdown: Any,
    opp_breakdown: Any,
    rp_1_pred: float,
    rp_2_pred: float,
    playoff: bool,
) -> float:
    # Applies caps to components, but EPAs still use the uncapped values
    # TODO: Compute and return standard deviation as well

    score = 0

    keys = all_keys[year]
    if year == 2016:
        score += min(6, breakdown[keys.index("auto_reach_points")])
        score += breakdown[keys.index("auto_crossing_points")]
        score += 5 * breakdown[keys.index("auto_low_boulders")]
        score += 10 * breakdown[keys.index("auto_high_boulders")]
        score += breakdown[keys.index("teleop_crossing_points")]
        score += 2 * breakdown[keys.index("teleop_low_boulders")]
        score += 5 * breakdown[keys.index("teleop_high_boulders")]
        score += min(45, breakdown[keys.index("endgame_points")])

        if playoff:
            score += rp_1_pred * 20
            score += rp_2_pred * 25

    elif year == 2017:
        score += min(15, breakdown[keys.index("auto_mobility_points")])
        score += breakdown[keys.index("auto_fuel_low")] / 3
        score += breakdown[keys.index("auto_fuel_high")]
        score += min(20, breakdown[keys.index("auto_rotor_points")])
        score += breakdown[keys.index("teleop_fuel_low")] / 9
        score += breakdown[keys.index("teleop_fuel_high")] / 3
        score += min(160, breakdown[keys.index("teleop_rotor_points")])
        score += min(150, breakdown[keys.index("takeoff_points")])

        if playoff:
            score += rp_1_pred * 20
            score += rp_2_pred * 100

    elif year == 2018:
        score += min(15, breakdown[keys.index("auto_run_points")])
        score += 2 * min(15, breakdown[keys.index("auto_switch_secs")])
        score += 2 * min(15, breakdown[keys.index("auto_scale_secs")])
        score += 145 * zero_sigmoid(
            breakdown[keys.index("switch_power")]
            - opp_breakdown[keys.index("opp_switch_power")]
        )
        score += 145 * zero_sigmoid(
            breakdown[keys.index("scale_power")]
            - opp_breakdown[keys.index("scale_power")]
        )
        score += min(45, breakdown[keys.index("vault_points")])
        score += min(90, breakdown[keys.index("endgame_points")])

    elif year == 2019:
        score += breakdown[keys.index("sandstorm_points")]
        score += 2 * min(8, breakdown[keys.index("bay_hatch")])
        score += 3 * min(8, breakdown[keys.index("bay_cargo")])
        score += 2 * min(4, breakdown[keys.index("rocket_hatch_low")])
        score += 2 * min(4, breakdown[keys.index("rocket_hatch_mid")])
        score += 2 * min(4, breakdown[keys.index("rocket_hatch_top")])
        score += 3 * min(4, breakdown[keys.index("rocket_cargo_low")])
        score += 3 * min(4, breakdown[keys.index("rocket_cargo_mid")])
        score += 3 * min(4, breakdown[keys.index("rocket_cargo_top")])
        score += min(36, breakdown[keys.index("hab_climb_points")])

    elif year == 2020:
        score += breakdown[keys.index("auto_init_line_points")]
        score += 2 * breakdown[keys.index("auto_cells_bottom")]
        score += 4 * breakdown[keys.index("auto_cells_outer")]
        score += 6 * breakdown[keys.index("auto_cells_inner")]
        score += breakdown[keys.index("teleop_cells_bottom")]
        score += 2 * breakdown[keys.index("teleop_cells_outer")]
        score += 3 * breakdown[keys.index("teleop_cells_inner")]
        score += min(20, breakdown[keys.index("control_panel_points")])
        score += min(90, breakdown[keys.index("endgame_points")])

    elif year == 2022:
        score += breakdown[keys.index("auto_taxi_points")]
        score += 2 * breakdown[keys.index("auto_cargo_lower")]
        score += 4 * breakdown[keys.index("auto_cargo_upper")]
        score += 1 * breakdown[keys.index("teleop_cargo_lower")]
        score += 2 * breakdown[keys.index("teleop_cargo_upper")]
        score += min(45, breakdown[keys.index("endgame_points")])

    elif year == 2023:
        score += breakdown[keys.index("auto_mobility_points")]
        score += breakdown[keys.index("auto_charge_station_points")]
        # row counts already enforced in post_process_breakdown()
        score += 3 * breakdown[keys.index("auto_low_cubes")]
        score += 3 * breakdown[keys.index("auto_low_cones")]
        score += 4 * breakdown[keys.index("auto_mid_cubes")]
        score += 4 * breakdown[keys.index("auto_mid_cones")]
        score += 6 * breakdown[keys.index("auto_high_cubes")]
        score += 6 * breakdown[keys.index("auto_high_cones")]
        score += 2 * breakdown[keys.index("teleop_low_cubes")]
        score += 2 * breakdown[keys.index("teleop_low_cones")]
        score += 3 * breakdown[keys.index("teleop_mid_cubes")]
        score += 3 * breakdown[keys.index("teleop_mid_cones")]
        score += 5 * breakdown[keys.index("teleop_high_cubes")]
        score += 5 * breakdown[keys.index("teleop_high_cones")]
        score += 5 * min(9, breakdown[keys.index("links")])
        score += min(30, breakdown[keys.index("endgame_charge_station_points")])

    else:
        score += breakdown[keys.index("no_foul_points")]

    return score
