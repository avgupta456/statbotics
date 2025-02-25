from typing import Any

# from typing import Tuple


from src.db.models import Year

# from src.models.epa.math import t_prob_gt_0
from src.models.epa.math import unit_sigmoid, zero_sigmoid
from src.tba.breakdown import all_keys

# from src.types.enums import EventType


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
        grid_points = breakdown[keys.index("grid_points")]
        teleop_grid_points += total_change
        cube_points += total_change * cube_points / grid_points
        cone_points += total_change * cone_points / grid_points
        grid_points += total_change

        breakdown[keys.index("bottom_pieces")] = bottom_pieces
        breakdown[keys.index("middle_pieces")] = middle_pieces
        breakdown[keys.index("top_pieces")] = top_pieces
        breakdown[keys.index("teleop_grid_points")] = teleop_grid_points
        breakdown[keys.index("cube_points")] = cube_points
        breakdown[keys.index("cone_points")] = cone_points
        breakdown[keys.index("grid_points")] = grid_points

    elif year == 2025:
        # we internally assign 3 points per processor algae. in reality, it's worth 6 points
        # for your alliance and 3 points for the opponent (assuming 75% success rate at 4 point net).
        # Adjust by adding 3 points per processor algae scored by both alliances
        my_processor_algae = breakdown[keys.index("processor_algae")]
        opp_processor_algae = opp_breakdown[keys.index("processor_algae")]
        processor_algae = my_processor_algae + opp_processor_algae
        breakdown[keys.index("processor_algae_points")] += 3 * my_processor_algae
        breakdown[keys.index("net_algae")] += 0.75 * opp_processor_algae
        breakdown[keys.index("net_algae_points")] += 3 * opp_processor_algae
        breakdown[keys.index("total_algae_points")] += 3 * processor_algae
        breakdown[keys.index("total_game_pieces")] += 0.75 * opp_processor_algae
        breakdown[keys.index("teleop_points")] += 3 * processor_algae
        total_change += 3 * processor_algae

    breakdown[0] += total_change

    return breakdown


"""
def get_pred_rps(
    year: int, week: int, event_type: EventType, breakdown_mean: Any, breakdown_sd: Any
) -> Tuple[float, float]:
    DISCOUNT = 0.85  # Teams try harder when near the threshold
    keys = all_keys[year]
    rp_1, rp_2 = 0, 0
    if year == 2016:
        boulders_mean = breakdown_mean[keys.index("boulders")]
        boulders_sd = breakdown_sd[keys.index("boulders")]

        rp_1 = breakdown_mean[keys.index("rp_1")]
        rp_2 = t_prob_gt_0(boulders_mean - 8 * DISCOUNT, boulders_sd)
        if event_type in [EventType.CHAMPS_DIV, EventType.EINSTEIN]:
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
        rocket_mean = breakdown_mean[keys.index("rocket_pieces")]
        rocket_sd = breakdown_sd[keys.index("rocket_pieces")]

        rp_1 = breakdown_mean[keys.index("rp_1")]
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
        if event_type in [EventType.CHAMPS_DIV, EventType.EINSTEIN]:
            rp_1 = t_prob_gt_0(links_mean - 5 * DISCOUNT, links_sd)

        rp_2 = breakdown_mean[keys.index("rp_2")]

    elif year == 2024:
        total_notes_mean = breakdown_mean[keys.index("total_notes")]
        total_notes_sd = breakdown_sd[keys.index("total_notes")]

        cutoff = 18  # 15 if coop but unlikely
        if event_type == EventType.DISTRICT_CMP:
            cutoff = 20  # 21, 18 if coop, somewhat likely
        elif event_type in [EventType.CHAMPS_DIV, EventType.EINSTEIN]:
            cutoff = 23  # 25, 21 if coop, fairly likely

        rp_1 = t_prob_gt_0(total_notes_mean - cutoff * DISCOUNT, total_notes_sd)

        rp_2 = breakdown_mean[keys.index("rp_2")]

    return rp_1, rp_2
"""


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

    if year.year == 2025:
        # modifies processor algae to be worth 3 points (from 6)
        update = 3 * err[keys.index("processor_algae")]  # loses 3 points per algae
        err[keys.index("processor_algae_points")] -= update
        err[keys.index("total_algae_points")] -= update
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
