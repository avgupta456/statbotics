from typing import Any

from src.db.models import Year
from src.models.epa.math import unit_sigmoid, zero_sigmoid
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
        if year >= 2025:
            breakdown[keys.index("rp_3")] = unit_sigmoid(breakdown[keys.index("rp_3")])

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
        bottom_pieces = breakdown[keys.index("bottom_pieces")]
        middle_pieces = breakdown[keys.index("middle_pieces")]
        top_pieces = breakdown[keys.index("top_pieces")]
        if top_pieces > 9:
            extra_top = top_pieces - 9
            middle_pieces += extra_top
            top_pieces = 9
            total_change -= 2 * extra_top
        if middle_pieces > 9:
            extra_mid = middle_pieces - 9
            bottom_pieces += extra_mid
            middle_pieces = 9
            total_change -= extra_mid
        if bottom_pieces > 9:
            extra_bot = bottom_pieces - 9
            middle_pieces += extra_bot
            bottom_pieces = 9
            total_change += extra_bot

        teleop_grid_points = breakdown[keys.index("teleop_grid_points")]
        cube_points = breakdown[keys.index("cube_points")]
        cone_points = breakdown[keys.index("cone_points")]
        grid_points = cube_points + cone_points  # computed inline (not a stored component)
        teleop_grid_points += total_change
        if grid_points > 0:
            cube_points += total_change * cube_points / grid_points
            cone_points += total_change * cone_points / grid_points

        breakdown[keys.index("bottom_pieces")] = bottom_pieces
        breakdown[keys.index("middle_pieces")] = middle_pieces
        breakdown[keys.index("top_pieces")] = top_pieces
        breakdown[keys.index("teleop_grid_points")] = teleop_grid_points
        breakdown[keys.index("cube_points")] = cube_points
        breakdown[keys.index("cone_points")] = cone_points

    elif year == 2025:
        # we internally assign 3 points per processor algae. in reality, it's worth 6 points
        # for your alliance and 3 points for the opponent (assuming 75% success rate at 4 point net).
        # Adjust by adding 3 points per processor algae scored by both alliances
        my_processor_algae = breakdown[keys.index("processor_algae")]
        opp_processor_algae = opp_breakdown[keys.index("processor_algae")]
        processor_algae = my_processor_algae + opp_processor_algae
        breakdown[keys.index("processor_algae_points")] += 3 * my_processor_algae
        breakdown[keys.index("net_algae_points")] += 3 * opp_processor_algae
        breakdown[keys.index("teleop_points")] += 3 * processor_algae
        total_change += 3 * processor_algae

    breakdown[0] += total_change

    return breakdown


def get_score_from_breakdown(
    key: str,
    year: int,
    breakdown: Any,
    opp_breakdown: Any,
    rp_1_pred: float,
    rp_2_pred: float,
    rp_3_pred: float,
    elim: bool,
) -> float:
    score = 0
    keys = all_keys[year]
    if year == 2016:
        score = breakdown[keys.index("no_foul_points")]
        if elim:
            score += rp_1_pred * 20
            score += rp_2_pred * 25
    elif year == 2017:
        score = breakdown[keys.index("no_foul_points")]
        if elim:
            score += rp_1_pred * 100
            score += rp_2_pred * 20
    elif year == 2018:
        score += min(15, breakdown[keys.index("auto_run_points")])
        score += 2 * min(15, breakdown[keys.index("auto_switch_secs")])
        score += 30 * zero_sigmoid(
            breakdown[keys.index("auto_scale_power")]
            - opp_breakdown[keys.index("auto_scale_power")]
        )
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
    elif year == 2020:
        score = breakdown[keys.index("no_foul_points")]
    elif year == 2022:
        score = breakdown[keys.index("no_foul_points")]
    elif year == 2023:
        score += breakdown[keys.index("auto_charge_station_points")]
        score += 2 * breakdown[keys.index("bottom_pieces")]
        score += 3 * breakdown[keys.index("middle_pieces")]
        score += 5 * breakdown[keys.index("top_pieces")]
        score += breakdown[keys.index("auto_pieces")]
        score += 5 * min(9, breakdown[keys.index("links")])
        score += min(30, breakdown[keys.index("endgame_charge_station_points")])
    elif year == 2024:
        score = breakdown[keys.index("no_foul_points")]
    else:
        score = breakdown[keys.index("no_foul_points")]

    return score


def post_process_attrib(year: Year, epa: Any, err: Any, elim: bool) -> Any:
    keys = all_keys[year.year]
    attrib = epa + err
    if year.year == 2018:
        # Overwrite total points using switch/scale power
        auto_index = keys.index("auto_points")
        teleop_index = keys.index("teleop_points")
        no_foul_index = keys.index("no_foul_points")

        attrib[auto_index] = (
            epa[keys.index("auto_run_points")]
            + 2 * epa[keys.index("auto_switch_secs")]
            + 30 * zero_sigmoid(epa[keys.index("auto_scale_power")] - year.comp_6_mean)
        )

        attrib[teleop_index] = (
            145 * zero_sigmoid(epa[keys.index("switch_power")] - year.comp_7_mean)
            + 145 * zero_sigmoid(epa[keys.index("scale_power")] - year.comp_8_mean)
            + epa[keys.index("vault_points")]
        )

        attrib[no_foul_index] = (
            attrib[auto_index]
            + attrib[teleop_index]
            + epa[keys.index("endgame_points")]
        )

    if year.year == 2025:
        # modifies processor algae to be worth 3 points (from 6)
        update = 3 * err[keys.index("processor_algae")]  # loses 3 points per algae
        err[keys.index("processor_algae_points")] -= update
        err[keys.index("teleop_points")] -= update
        err[keys.index("no_foul_points")] -= update
        attrib = epa + err

    if year.year >= 2016 and elim:
        # Don't update RP score during elim match
        rp_1_index = keys.index("rp_1")
        attrib[rp_1_index] = epa[rp_1_index]

        rp_2_index = keys.index("rp_2")
        attrib[rp_2_index] = epa[rp_2_index]

        if year.year >= 2025:
            rp_3_index = keys.index("rp_3")
            attrib[rp_3_index] = epa[rp_3_index]

    return attrib
