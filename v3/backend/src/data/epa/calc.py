from collections import defaultdict
from typing import Dict

from src.models.epa_v2.main import EPAV2

from src.data.utils import objs_type
from src.db.models import TeamYear, TeamMatch, Alliance, TeamEvent
from src.utils.utils import get_team_match_key, get_team_event_key, get_team_year_key


def process_year(
    objs: objs_type, all_team_years: Dict[int, Dict[str, TeamYear]]
) -> objs_type:
    year = objs[0]
    team_years = objs[1]
    team_events = objs[3]
    matches = objs[4]
    alliances = objs[5]
    team_matches = objs[6]

    match_red_alliance: Dict[str, Alliance] = {}
    match_blue_alliance: Dict[str, Alliance] = {}
    for alliance in alliances.values():
        if alliance.alliance == "red":
            match_red_alliance[alliance.match] = alliance
        else:
            match_blue_alliance[alliance.match] = alliance

    match_team_matches: Dict[str, Dict[str, TeamMatch]] = defaultdict(dict)
    match_team_events: Dict[str, Dict[str, TeamEvent]] = defaultdict(dict)
    match_team_years: Dict[str, Dict[str, TeamYear]] = defaultdict(dict)
    for match in matches.values():
        red_teams, blue_teams = match.get_teams()
        for team in red_teams + blue_teams:
            team_match_key = get_team_match_key(team, match.key)
            match_team_matches[match.key][team] = team_matches[team_match_key]
            team_event_key = get_team_event_key(team, match.event)
            match_team_events[match.key][team] = team_events[team_event_key]
            team_year_key = get_team_year_key(team, match.year)
            match_team_years[match.key][team] = team_years[team_year_key]

    model = EPAV2()

    model.start_season(year, all_team_years, team_years)
    for curr_match in sorted(matches.values(), key=lambda m: m.time):
        curr_red_alliance = match_red_alliance[curr_match.key]
        curr_blue_alliance = match_blue_alliance[curr_match.key]
        curr_team_matches = match_team_matches[curr_match.key]
        curr_team_events = match_team_events[curr_match.key]
        curr_team_years = match_team_years[curr_match.key]
        model.process_match(
            curr_match,
            curr_red_alliance,
            curr_blue_alliance,
            curr_team_matches,
            curr_team_events,
            curr_team_years,
        )
    model.end_season(year, team_years)

    return objs

    # def process_year(
    #     objs: objs_type, all_team_years: Dict[int, Dict[str, TeamYear]]
    # ) -> objs_type:
    #     # TODO: Component EPAs
    #     # TODO: Error bars

    #     year = objs[0]
    #     team_years = objs[1]
    #     matches = objs[4]
    #     team_matches = objs[6]

    #     year_num = year.year

    #     NUM_TEAMS = 2 if year_num <= 2004 else 3
    #     USE_COMPONENTS = year_num >= 2016
    #     K = k_func(year_num)

    #     sd = year.score_sd or 0

    #     init_rating = get_init_epa(year, None, None)
    #     team_epas: Dict[str, Rating] = defaultdict(lambda: init_rating)

    #     alliance_ids: Dict[str, List[Rating]] = defaultdict(list)
    #     team_match_ids: Dict[str, Rating] = {}
    #     team_match_ids_post: Dict[str, float] = {}

    #     # INITIALIZE
    #     for team_year in team_years.values():
    #         num = team_year.team

    #         past_team_years: List[TeamYear] = []
    #         for past_year in range(year_num - 1, year_num - 5, -1):
    #             past_team_year = all_team_years.get(past_year, {}).get(num, None)
    #             if past_team_year is not None:
    #                 past_team_years.append(past_team_year)

    #         past_team_year_1 = past_team_years[0] if len(past_team_years) > 0 else None
    #         past_team_year_2 = past_team_years[1] if len(past_team_years) > 1 else None

    #         rating = get_init_epa(year, past_team_year_1, past_team_year_2)

    #         team_epas[num] = rating
    #         team_year.epa_start = r(rating.epa.mean[0], 2)

    #         if USE_COMPONENTS:
    #             team_year.rp_1_epa_start = r(rating.rp_1 or -1, 4)
    #             team_year.rp_2_epa_start = r(rating.rp_2 or -1, 4)

    #     # MATCHES
    #     sorted_matches = sorted(matches.values(), key=lambda m: m.sort())
    #     for m in sorted_matches:
    #         red, blue = m.get_teams()

    #         red_epa_pre: Dict[str, Rating] = {}
    #         blue_epa_pre: Dict[str, Rating] = {}

    #         for t in red:
    #             red_epa_pre[t] = team_epas[t]
    #             alliance_ids[get_alliance_key(m.key, AllianceColor.RED)].append(
    #                 team_epas[t]
    #             )
    #             team_match_ids[get_team_match_key(t, m.key)] = team_epas[t]
    #             team_match_ids_post[get_team_match_key(t, m.key)] = team_epas[t].epa.mean[0]
    #         for t in blue:
    #             blue_epa_pre[t] = team_epas[t]
    #             alliance_ids[get_alliance_key(m.key, AllianceColor.BLUE)].append(
    #                 team_epas[t]
    #             )
    #             team_match_ids[get_team_match_key(t, m.key)] = team_epas[t]
    #             team_match_ids_post[get_team_match_key(t, m.key)] = team_epas[t].epa.mean[0]

    #         red = red[:NUM_TEAMS]
    #         blue = blue[:NUM_TEAMS]

    #         red_epa_sum = sum([x.epa.mean[0] for x in red_epa_pre.values()])
    #         blue_epa_sum = sum([x.epa.mean[0] for x in blue_epa_pre.values()])

    #         m.red_score_pred = r(red_epa_sum, 2)
    #         m.blue_score_pred = r(blue_epa_sum, 2)

    #         if USE_COMPONENTS:
    #             red_rp_1_epa_sum = sum([x.rp_1 or 0 for x in red_epa_pre.values()])
    #             blue_rp_1_epa_sum = sum([x.rp_1 or 0 for x in blue_epa_pre.values()])
    #             red_rp_2_epa_sum = sum([x.rp_2 or 0 for x in red_epa_pre.values()])
    #             blue_rp_2_epa_sum = sum([x.rp_2 or 0 for x in blue_epa_pre.values()])

    #             m.red_rp_1_pred = r(sigmoid(red_rp_1_epa_sum), 4)
    #             m.blue_rp_1_pred = r(sigmoid(blue_rp_1_epa_sum), 4)
    #             m.red_rp_2_pred = r(sigmoid(red_rp_2_epa_sum), 4)
    #             m.blue_rp_2_pred = r(sigmoid(blue_rp_2_epa_sum), 4)

    #         norm_diff = (m.red_score_pred - m.blue_score_pred) / sd
    #         win_prob = 1 / (1 + 10 ** (K * norm_diff))

    #         m.epa_win_prob = r(win_prob, 4)
    #         m.epa_winner = MatchWinner.RED if win_prob >= 0.5 else MatchWinner.BLUE

    #         if m.status != MatchStatus.COMPLETED:
    #             continue

    #         weight = ELIM_WEIGHT if m.elim else 1
    #         rp_weight = 0 if m.elim else 1

    #         red_err = (m.red_no_foul or m.red_score or 0) - m.red_score_pred
    #         blue_err = (m.blue_no_foul or m.blue_score or 0) - m.blue_score_pred
    #         # TODO: don't run RP calc if not USE_COMPONENTS
    #         red_rp_1_err = (m.red_rp_1 or 0) - (m.red_rp_1_pred or 0)
    #         red_rp_2_err = (m.red_rp_2 or 0) - (m.red_rp_2_pred or 0)
    #         blue_rp_1_err = (m.blue_rp_1 or 0) - (m.blue_rp_1_pred or 0)
    #         blue_rp_2_err = (m.blue_rp_2 or 0) - (m.blue_rp_2_pred or 0)

    #         # If any, do not update EPA values
    #         placeholder_match = len(set(PLACEHOLDER_TEAMS).intersection(set(red + blue))) > 0
    #         elim_dq = m.elim and (
    #             len(m.get_red_dqs()) == NUM_TEAMS or len(m.get_blue_dqs()) == NUM_TEAMS
    #         )
    #         skip_update = placeholder_match or elim_dq or m.offseason

    #         for teams, err, rp_1_err, rp_2_err, epa_pre in [
    #             (red, red_err, red_rp_1_err, red_rp_2_err, red_epa_pre),
    #             (blue, blue_err, blue_rp_1_err, blue_rp_2_err, blue_epa_pre),
    #         ]:
    #             for t in teams:
    #                 team_count = team_epas[t].count
    #                 percent = percent_func(year_num, team_count)
    #                 epa_alpha = weight * percent / NUM_TEAMS
    #                 new_epa = epa_pre[t][0] + err * epa_alpha

    #                 rp_alpha = rp_weight * RP_PERCENT / NUM_TEAMS
    #                 new_rp_1_epa = epa_pre[t][1] + rp_1_err * rp_alpha
    #                 new_rp_2_epa = epa_pre[t][2] + rp_2_err * rp_alpha

    #                 if skip_update:
    #                     new_epa = epa_pre[t][0]
    #                     new_rp_1_epa = epa_pre[t][1]
    #                     new_rp_2_epa = epa_pre[t][2]

    #                 new_rating = Rating(new_epa, new_rp_1_epa, new_rp_2_epa)
    #                 team_epas[t] = new_rating

    #                 team_match_ids_post[get_team_match_key(t, m.key)] = new_epa

    #                 if not m.elim and not skip_update:
    #                     team_epas[t].count += 1

    # # TEAM MATCHES
    # for team_match in team_matches.values():
    #     team_match_key = get_team_match_key(team_match.team, team_match.match)
    #     rating = team_match_ids.get(team_match_key, None)
    #     team_match.epa = r(rating.epa.mean[0] if rating else -1, 2)
    #     if team_match.status == MatchStatus.COMPLETED:
    #         team_match.post_epa = r(team_match_ids_post.get(team_match_key, -1), 2)

    #     if USE_COMPONENTS:
    #         team_match.rp_1_epa = r(rating.rp_1 or -1 if rating else -1, 4)
    #         team_match.rp_2_epa = r(rating.rp_2 or -1 if rating else -1, 4)

    # return objs
