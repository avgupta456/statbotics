from typing import Any, Tuple

from src.models.epa_v2.math import t_prob_gt_0, zero_sigmoid
from src.tba.breakdown import all_keys
from src.db.models import Year

for year in range(2002, 2024):
    if len(all_keys[year]) > 23:
        # 5 standard (total, auto, teleop, endgame, tiebreaker) + 18 components
        raise ValueError(f"Too many keys for year {year}")
    all_keys[year] += ["empty"] * (23 - len(all_keys[year]))


def post_process_breakdown(
    year: int, key: str, breakdown: Any, opp_breakdown: Any
) -> Any:
    # Updates breakdown for both score prediction and EPA update

    keys = all_keys[year]
    total_change = 0

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
