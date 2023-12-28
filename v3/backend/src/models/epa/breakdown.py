from typing import Any, Tuple

from src.db.models import Year
from src.models.epa.math import t_prob_gt_0, unit_sigmoid, zero_sigmoid
from src.tba.breakdown import all_keys


def post_process_breakdown(
    year: int, key: str, breakdown: Any, opp_breakdown: Any
) -> Any:
    # Updates breakdown for both score prediction and EPA update

    keys = all_keys[year]
    total_change = 0

    if year >= 2016:
        breakdown[keys.index("rp_1")] = unit_sigmoid(breakdown[keys.index("rp_1")])
        breakdown[keys.index("rp_2")] = unit_sigmoid(breakdown[keys.index("rp_2")])

    if year == 2018:
        my_switch_power = breakdown[keys.index("switch_power")]
        opp_opp_switch_power = opp_breakdown[keys.index("opp_switch_power")]
        new_switch_power = zero_sigmoid(my_switch_power - opp_opp_switch_power)

        my_scale_power = breakdown[keys.index("scale_power")]
        opp_scale_power = opp_breakdown[keys.index("scale_power")]
        new_scale_power = zero_sigmoid(my_scale_power - opp_scale_power)

        my_opp_switch_power = breakdown[keys.index("opp_switch_power")]
        opp_switch_power = opp_breakdown[keys.index("switch_power")]
        new_opp_switch_power = zero_sigmoid(my_opp_switch_power - opp_switch_power)

        breakdown[keys.index("switch_power")] = new_switch_power
        breakdown[keys.index("scale_power")] = new_scale_power
        breakdown[keys.index("opp_switch_power")] = new_opp_switch_power

    elif year == 2023:
        # atcui = Auto Top CUbes Index, etc
        atcui = keys.index("auto_top_cubes")
        atcoi = keys.index("auto_top_cones")
        ttcui = keys.index("teleop_top_cubes")
        ttcoi = keys.index("teleop_top_cones")
        amcui = keys.index("auto_mid_cubes")
        amcoi = keys.index("auto_mid_cones")
        tmcui = keys.index("teleop_mid_cubes")
        tmcoi = keys.index("teleop_mid_cones")
        abcui = keys.index("auto_bot_cubes")
        abcoi = keys.index("auto_bot_cones")
        tbcui = keys.index("teleop_bot_cubes")
        tbcoi = keys.index("teleop_bot_cones")

        auto_top = breakdown[atcui] + breakdown[atcoi]
        teleop_top = breakdown[ttcui] + breakdown[ttcoi]
        total_top = auto_top + teleop_top

        if total_top > 9:
            teleop_mid = breakdown[tmcui] + breakdown[tmcoi]
            extra_top = total_top - 9
            breakdown[ttcui] *= (9 - auto_top) / teleop_top
            breakdown[ttcoi] *= (9 - auto_top) / teleop_top
            breakdown[tmcui] *= (teleop_mid + extra_top) / teleop_mid
            breakdown[tmcoi] *= (teleop_mid + extra_top) / teleop_mid

            # each game piece moving from top to mid is 2 points lost
            total_change -= extra_top * 2

        auto_mid = breakdown[amcui] + breakdown[amcoi]
        teleop_mid = breakdown[tmcui] + breakdown[tmcoi]
        total_mid = auto_mid + teleop_mid
        if total_mid > 9:
            teleop_bot = breakdown[tbcui] + breakdown[tbcoi]
            extra_mid = total_mid - 9
            breakdown[tmcui] *= (9 - auto_mid) / teleop_mid
            breakdown[tmcoi] *= (9 - auto_mid) / teleop_mid
            breakdown[tbcui] *= (teleop_bot + extra_mid) / teleop_bot
            breakdown[tbcoi] *= (teleop_bot + extra_mid) / teleop_bot

            # each game piece moving from mid to bottom is 1 point lost
            total_change -= extra_mid

        auto_bot = breakdown[abcui] + breakdown[abcoi]
        teleop_bot = breakdown[tbcui] + breakdown[tbcoi]
        total_bot = auto_bot + teleop_bot
        if total_bot > 9 and total_mid > 9 and total_top > 9:
            extra_bot = total_bot - 9
            breakdown[tbcui] *= (9 - auto_bot) / teleop_bot
            breakdown[tbcoi] *= (9 - auto_bot) / teleop_bot
            # supercharge counts as mid cubes
            breakdown[tmcui] += extra_bot
            # each game piece moving from bottom to supercharge is 1 point gained
            total_change += extra_bot

    breakdown[0] += total_change

    return breakdown


def get_pred_rps(
    year: int, week: int, breakdown_mean: Any, breakdown_sd: Any
) -> Tuple[float, float]:
    DISCOUNT = 0.85  # Teams try harder when near the threshold
    keys = all_keys[year]
    rp_1, rp_2 = 0, 0
    if year == 2016:
        boulders_mean = breakdown_mean[keys.index("boulders")]
        boulders_sd = breakdown_sd[keys.index("boulders")]

        rp_1 = breakdown_mean[keys]
        rp_2 = t_prob_gt_0(boulders_mean - 8 * DISCOUNT, boulders_sd)
        if week >= 8:
            rp_2 = t_prob_gt_0(boulders_mean - 10 * DISCOUNT, boulders_sd)

    elif year == 2017:
        kpa_mean = breakdown_mean[keys.index("kpa")]
        kpa_sd = breakdown_sd[keys.index("kpa")]

        gears_mean = breakdown_mean[keys.index("gears")]
        gears_sd = breakdown_sd[keys.index("gears")]

        rp_1 = t_prob_gt_0(kpa_mean - 40 * DISCOUNT, kpa_sd)
        rp_2 = t_prob_gt_0(gears_mean - 13 * DISCOUNT, gears_sd)

    elif year == 2018:
        rp_1 = breakdown_mean[keys.index("rp_1")]
        rp_2 = breakdown_mean[keys.index("rp_2")]

    elif year == 2019:
        rocket_mean = breakdown_mean[keys.index("rocket")]
        rocket_sd = breakdown_sd[keys.index("rocket")]

        rp_1 = breakdown_mean[keys.index("rp_1")]
        # assume bottom is easy, top is attempted less since no incentive
        rp_2 = t_prob_gt_0(rocket_mean - 12 * DISCOUNT, rocket_sd)

    elif year == 2020:
        rp_1 = breakdown_mean[keys.index("rp_1")]
        rp_2 = breakdown_mean[keys.index("rp_2")]

    elif year == 2022:
        cargo_mean = breakdown_mean[keys.index("cargo")]
        cargo_sd = breakdown_sd[keys.index("cargo")]

        rp_1 = t_prob_gt_0(cargo_mean - 20 * DISCOUNT, cargo_sd)
        rp_2 = breakdown_mean[keys.index("rp_2")]

    elif year == 2023:
        links_mean = breakdown_mean[keys.index("links")]
        links_sd = breakdown_sd[keys.index("links")]

        rp_1 = t_prob_gt_0(links_mean - 4 * DISCOUNT, links_sd)
        if week >= 8:
            rp_1 = t_prob_gt_0(links_mean - 5 * DISCOUNT, links_sd)

        rp_2 = breakdown_mean[keys.index("rp_2")]

    return rp_1, rp_2


def get_score_from_breakdown(
    key: str,
    year: int,
    breakdown: Any,
    opp_breakdown: Any,
    rp_1_pred: float,
    rp_2_pred: float,
    elim: bool,
) -> float:
    # Applies caps to components, but EPAs still use the uncapped values
    # TODO: Compute and return standard deviation as well

    score = 0
    keys = all_keys[year]
    if year == 2016:
        score = breakdown[keys.index("no_foul_points")]
        """
        score += min(6, breakdown[keys.index("auto_reach_points")])
        score += breakdown[keys.index("auto_crossing_points")]
        score += 5 * breakdown[keys.index("auto_low_boulders")]
        score += 10 * breakdown[keys.index("auto_high_boulders")]
        score += breakdown[keys.index("teleop_crossing_points")]
        score += 2 * breakdown[keys.index("teleop_low_boulders")]
        score += 5 * breakdown[keys.index("teleop_high_boulders")]
        score += min(45, breakdown[keys.index("endgame_points")])
        """
        if elim:
            score += rp_1_pred * 20
            score += rp_2_pred * 25
    elif year == 2017:
        score = breakdown[keys.index("no_foul_points")]
        """
        score += min(15, breakdown[keys.index("auto_mobility_points")])
        score += breakdown[keys.index("auto_fuel_low")] / 3
        score += breakdown[keys.index("auto_fuel_high")]
        score += min(20, breakdown[keys.index("auto_rotor_points")])
        score += breakdown[keys.index("teleop_fuel_low")] / 9
        score += breakdown[keys.index("teleop_fuel_high")] / 3
        score += min(160, breakdown[keys.index("teleop_rotor_points")])
        score += min(150, breakdown[keys.index("takeoff_points")])
        """
        if elim:
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
        score = breakdown[keys.index("no_foul_points")]
        """
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
        """
    elif year == 2020:
        score = breakdown[keys.index("no_foul_points")]
        """
        score += breakdown[keys.index("auto_init_line_points")]
        score += 2 * breakdown[keys.index("auto_cells_bottom")]
        score += 4 * breakdown[keys.index("auto_cells_outer")]
        score += 6 * breakdown[keys.index("auto_cells_inner")]
        score += breakdown[keys.index("teleop_cells_bottom")]
        score += 2 * breakdown[keys.index("teleop_cells_outer")]
        score += 3 * breakdown[keys.index("teleop_cells_inner")]
        score += min(20, breakdown[keys.index("control_panel_points")])
        score += min(90, breakdown[keys.index("endgame_points")])
        """
    elif year == 2022:
        score = breakdown[keys.index("no_foul_points")]
        """
        score += breakdown[keys.index("auto_taxi_points")]
        score += 2 * breakdown[keys.index("auto_cargo_lower")]
        score += 4 * breakdown[keys.index("auto_cargo_upper")]
        score += 1 * breakdown[keys.index("teleop_cargo_lower")]
        score += 2 * breakdown[keys.index("teleop_cargo_upper")]
        score += min(45, breakdown[keys.index("endgame_points")])
        """
    elif year == 2023:
        score += breakdown[keys.index("auto_mobility_points")]
        score += breakdown[keys.index("auto_charge_station_points")]
        # row counts already enforced in post_process_breakdown()
        score += 3 * breakdown[keys.index("auto_bot_cubes")]
        score += 3 * breakdown[keys.index("auto_bot_cones")]
        score += 4 * breakdown[keys.index("auto_mid_cubes")]
        score += 4 * breakdown[keys.index("auto_mid_cones")]
        score += 6 * breakdown[keys.index("auto_top_cubes")]
        score += 6 * breakdown[keys.index("auto_top_cones")]
        score += 2 * breakdown[keys.index("teleop_bot_cubes")]
        score += 2 * breakdown[keys.index("teleop_bot_cones")]
        score += 3 * breakdown[keys.index("teleop_mid_cubes")]
        score += 3 * breakdown[keys.index("teleop_mid_cones")]
        score += 5 * breakdown[keys.index("teleop_top_cubes")]
        score += 5 * breakdown[keys.index("teleop_top_cones")]
        score += 5 * min(9, breakdown[keys.index("links")])
        score += min(30, breakdown[keys.index("endgame_charge_station_points")])
    else:
        score += breakdown[keys.index("no_foul_points")]

    return score


def post_process_attrib(year: Year, epa: Any, attrib: Any, elim: bool) -> Any:
    keys = all_keys[year.year]
    if year.year == 2018:
        # Overwrite total points using switch/scale power
        auto_index = keys.index("auto_points")
        teleop_index = keys.index("teleop_points")
        no_foul_index = keys.index("no_foul_points")

        attrib[auto_index] = (
            epa[keys.index("auto_run_points")]
            + 2 * epa[keys.index("auto_switch_secs")]
            + 30 * zero_sigmoid(epa[keys.index("auto_scale_power")] - year.comp_7_mean)
        )

        attrib[teleop_index] = (
            145 * zero_sigmoid(epa[keys.index("switch_power")] - year.comp_8_mean)
            + 145 * zero_sigmoid(epa[keys.index("scale_power")] - year.comp_9_mean)
            + epa[keys.index("vault_points")]
        )

        attrib[no_foul_index] = (
            attrib[auto_index]
            + attrib[teleop_index]
            + epa[keys.index("endgame_points")]
        )

    return attrib
