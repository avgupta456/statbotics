from collections import defaultdict
from typing import Dict, List, Tuple

from src.types.enums import MatchStatus, AllianceColor, MatchWinner
from src.data.utils import objs_type
from src.db.models import TeamYear
from src.epa.constants import ELIM_WEIGHT, RP_PERCENT
from src.epa.init import get_init_epa
from src.epa.main import k_func, percent_func
from src.epa.math import sigmoid
from src.epa.types import Rating
from src.tba.constants import OFFSEASON_TEAMS
from src.utils.utils import get_alliance_key, get_team_match_key


def process_year(
    objs: objs_type, all_team_years: Dict[int, Dict[str, TeamYear]]
) -> objs_type:
    # TODO: Figure out why performance is worse than prod
    # TODO: Component EPAs
    # TODO: Error bars

    year = objs[0]
    team_years = objs[1]
    events = objs[2]
    matches = objs[4]
    alliances = objs[5]
    team_matches = objs[6]

    year_num = year.year

    NUM_TEAMS = 2 if year_num <= 2004 else 3
    USE_COMPONENTS = year_num >= 2016
    K = k_func(year_num)

    sd = year.score_sd or 0

    init_rating = get_init_epa(year, None, None)
    team_epas: Dict[str, Rating] = defaultdict(lambda: init_rating)

    alliance_ids: Dict[str, List[Rating]] = defaultdict(list)
    team_match_ids: Dict[str, Rating] = {}
    team_match_ids_post: Dict[str, float] = {}

    # INITIALIZE
    for team_year in team_years.values():
        num = team_year.team

        past_team_years: List[TeamYear] = []
        for past_year in range(year_num - 1, year_num - 5, -1):
            past_team_year = all_team_years.get(past_year, {}).get(num, None)
            if past_team_year is not None:
                past_team_years.append(past_team_year)

        past_team_year_1 = past_team_years[0] if len(past_team_years) > 0 else None
        past_team_year_2 = past_team_years[1] if len(past_team_years) > 1 else None

        rating = get_init_epa(year, past_team_year_1, past_team_year_2)

        team_epas[num] = rating
        team_year.epa_start = round(rating.epa, 2)

        if USE_COMPONENTS:
            team_year.rp_1_epa_start = round(rating.rp_1, 4)
            team_year.rp_2_epa_start = round(rating.rp_2, 4)

    # MATCHES
    event_offseason = {e.key: e.offseason for e in events.values()}
    sorted_matches = sorted(matches.values(), key=lambda m: m.sort())
    for m in sorted_matches:
        red, blue = m.get_teams()

        red_epa_pre: Dict[str, Tuple[float, float, float]] = {}
        blue_epa_pre: Dict[str, Tuple[float, float, float]] = {}

        for t in red:
            red_epa_pre[t] = (team_epas[t].epa, team_epas[t].rp_1, team_epas[t].rp_2)
            alliance_ids[get_alliance_key(m.key, AllianceColor.RED)].append(
                team_epas[t]
            )
            team_match_ids[get_team_match_key(t, m.key)] = team_epas[t]
        for t in blue:
            blue_epa_pre[t] = (team_epas[t].epa, team_epas[t].rp_1, team_epas[t].rp_2)
            alliance_ids[get_alliance_key(m.key, AllianceColor.BLUE)].append(
                team_epas[t]
            )
            team_match_ids[get_team_match_key(t, m.key)] = team_epas[t]
            team_match_ids_post[get_team_match_key(t, m.key)] = team_epas[t].epa

        red = red[:NUM_TEAMS]
        blue = blue[:NUM_TEAMS]

        red_epa_sum = sum([x[0] for x in red_epa_pre.values()])
        blue_epa_sum = sum([x[0] for x in blue_epa_pre.values()])

        m.red_score_pred = round(red_epa_sum, 2)
        m.blue_score_pred = round(blue_epa_sum, 2)

        if USE_COMPONENTS:
            red_rp_1_epa_sum = sum([x[1] for x in red_epa_pre.values()])
            blue_rp_1_epa_sum = sum([x[1] for x in blue_epa_pre.values()])
            red_rp_2_epa_sum = sum([x[2] for x in red_epa_pre.values()])
            blue_rp_2_epa_sum = sum([x[2] for x in blue_epa_pre.values()])

            m.red_rp_1_pred = round(sigmoid(red_rp_1_epa_sum), 4)
            m.blue_rp_1_pred = round(sigmoid(blue_rp_1_epa_sum), 4)
            m.red_rp_2_pred = round(sigmoid(red_rp_2_epa_sum), 4)
            m.blue_rp_2_pred = round(sigmoid(blue_rp_2_epa_sum), 4)

        norm_diff = (m.red_score_pred - m.blue_score_pred) / sd
        win_prob = 1 / (1 + 10 ** (K * norm_diff))

        m.epa_win_prob = round(win_prob, 4)
        m.epa_winner = MatchWinner.RED if win_prob >= 0.5 else MatchWinner.BLUE

        if m.status != MatchStatus.COMPLETED:
            continue

        weight = ELIM_WEIGHT if m.elim else 1
        rp_weight = 0 if m.elim else 1

        red_err = (m.red_no_foul or m.red_score or 0) - m.red_score_pred
        blue_err = (m.blue_no_foul or m.blue_score or 0) - m.blue_score_pred
        # TODO: don't run RP calc if not USE_COMPONENTS
        red_rp_1_err = (m.red_rp_1 or 0) - (m.red_rp_1_pred or 0)
        red_rp_2_err = (m.red_rp_2 or 0) - (m.red_rp_2_pred or 0)
        blue_rp_1_err = (m.blue_rp_1 or 0) - (m.blue_rp_1_pred or 0)
        blue_rp_2_err = (m.blue_rp_2 or 0) - (m.blue_rp_2_pred or 0)

        # If any, do not update EPA values
        placeholder_match = len(set(OFFSEASON_TEAMS).intersection(set(red + blue))) > 0
        elim_dq = m.elim and (
            len(m.get_red_dqs()) == NUM_TEAMS or len(m.get_blue_dqs()) == NUM_TEAMS
        )
        offseason_event = event_offseason[m.event]
        skip_update = placeholder_match or elim_dq or offseason_event

        for teams, err, rp_1_err, rp_2_err, epa_pre in [
            (red, red_err, red_rp_1_err, red_rp_2_err, red_epa_pre),
            (blue, blue_err, blue_rp_1_err, blue_rp_2_err, blue_epa_pre),
        ]:
            for t in teams:
                team_count = team_epas[t].count
                percent = percent_func(year_num, team_count)
                epa_alpha = weight * percent / NUM_TEAMS
                new_epa = epa_pre[t][0] + err * epa_alpha

                rp_alpha = rp_weight * RP_PERCENT / NUM_TEAMS
                new_rp_1_epa = epa_pre[t][1] + rp_1_err * rp_alpha
                new_rp_2_epa = epa_pre[t][2] + rp_2_err * rp_alpha

                if skip_update:
                    new_epa = epa_pre[t][0]
                    new_rp_1_epa = epa_pre[t][1]
                    new_rp_2_epa = epa_pre[t][2]

                new_rating = Rating(new_epa, new_rp_1_epa, new_rp_2_epa)
                team_epas[t] = new_rating

                team_match_ids_post[get_team_match_key(t, m.key)] = new_epa

                if not m.elim and not skip_update:
                    team_epas[t].count += 1

    # ALLIANCES
    for a in alliances.values():
        is_red = a.alliance == AllianceColor.RED
        m = matches[a.match]
        if m.epa_win_prob is not None:
            a.epa_win_prob = m.epa_win_prob if is_red else round(1 - m.epa_win_prob, 4)
        a.epa_winner = m.epa_winner
        a.score_pred = m.red_score_pred if is_red else m.blue_score_pred
        if USE_COMPONENTS:
            a.rp_1_pred = m.red_rp_1_pred if is_red else m.blue_rp_1_pred
            a.rp_2_pred = m.red_rp_2_pred if is_red else m.blue_rp_2_pred

    # TEAM MATCHES
    for team_match in team_matches.values():
        team_match_key = get_team_match_key(team_match.team, team_match.match)
        rating = team_match_ids.get(team_match_key, None)
        team_match.epa = round(rating.epa if rating else -1, 2)
        if team_match.status == MatchStatus.COMPLETED:
            team_match.post_epa = round(team_match_ids_post.get(team_match_key, -1), 2)

        if USE_COMPONENTS:
            team_match.rp_1_epa = round(rating.rp_1 if rating else -1, 4)
            team_match.rp_2_epa = round(rating.rp_2 if rating else -1, 4)

    return objs
