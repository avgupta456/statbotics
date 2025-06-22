from collections import defaultdict
from typing import Dict, List, Tuple

from src.constants import CURR_WEEK, CURR_YEAR
from src.data.utils import objs_type
from src.db.models import Event, Match, Team, TeamEvent, TeamYear
from src.types.enums import EventStatus, MatchStatus, MatchWinner
from src.utils.utils import r


def winrate(wins: int, ties: int, count: int) -> float:
    return r((wins + ties / 2) / max(1, count), 4)


TRecord = Tuple[int, int, int, int]
TRP = Tuple[int, int]


def process_year(objs: objs_type) -> objs_type:
    year_num = objs[0].year
    event_to_week = {e.key: e.week for e in objs[2].values()}

    ty_record: Dict[int, TRecord] = defaultdict(lambda: (0, 0, 0, 0))
    te_record: Dict[Tuple[int, str], TRecord] = defaultdict(lambda: (0, 0, 0, 0))
    te_qual_record: Dict[Tuple[int, str], TRecord] = defaultdict(lambda: (0, 0, 0, 0))
    te_rps: Dict[Tuple[int, str], TRP] = defaultdict(lambda: (0, 0))

    for m_obj in objs[4].values():
        elim = m_obj.elim
        event = m_obj.event
        status = m_obj.status
        winner = m_obj.winner

        if (
            event_to_week[event] == 9
            or status != MatchStatus.COMPLETED
            or winner is None
        ):
            continue

        for alliance in ["red", "blue"]:
            teams = m_obj.get_red() if alliance == "red" else m_obj.get_blue()
            if year_num <= 2004:
                teams = teams[:2]  # 2 team alliances

            dqs = m_obj.get_red_dqs() if alliance == "red" else m_obj.get_blue_dqs()
            surrogates = (
                m_obj.get_red_surrogates()
                if alliance == "red"
                else m_obj.get_blue_surrogates()
            )

            win_update = 1 if alliance == winner else 0
            tie_update = 1 if winner == MatchWinner.TIE else 0
            loss_update = 1 - win_update - tie_update

            rp_1 = (m_obj.red_rp_1 if alliance == "red" else m_obj.blue_rp_1) or 0
            rp_2 = (m_obj.red_rp_2 if alliance == "red" else m_obj.blue_rp_2) or 0
            rp_3 = (m_obj.red_rp_3 if alliance == "red" else m_obj.blue_rp_3) or 0
            win_rps = 3 if year_num >= 2025 else 2
            total_rps = win_rps * win_update + 1 * tie_update + rp_1 + rp_2 + rp_3

            for t in teams:
                ty_record[t] = (
                    ty_record[t][0] + win_update,
                    ty_record[t][1] + loss_update,
                    ty_record[t][2] + tie_update,
                    ty_record[t][3] + 1,
                )

                if t not in dqs and t not in surrogates:
                    # DQ, surrogate only affect TeamEvent records
                    te_record[(t, event)] = (
                        te_record[(t, event)][0] + win_update,
                        te_record[(t, event)][1] + loss_update,
                        te_record[(t, event)][2] + tie_update,
                        te_record[(t, event)][3] + 1,
                    )
                    if not elim:
                        te_qual_record[(t, event)] = (
                            te_qual_record[(t, event)][0] + win_update,
                            te_qual_record[(t, event)][1] + loss_update,
                            te_qual_record[(t, event)][2] + tie_update,
                            te_qual_record[(t, event)][3] + 1,
                        )
                        te_rps[(t, event)] = (
                            te_rps[(t, event)][0] + total_rps,
                            te_rps[(t, event)][1] + 1,
                        )

    for team_year in objs[1].values():
        (
            team_year.wins,
            team_year.losses,
            team_year.ties,
            team_year.count,
        ) = ty_record[team_year.team]
        team_year.winrate = winrate(team_year.wins, team_year.ties, team_year.count)

    for team_event in objs[3].values():
        (
            team_event.wins,
            team_event.losses,
            team_event.ties,
            team_event.count,
        ) = te_record[(team_event.team, team_event.event)]
        team_event.winrate = winrate(team_event.wins, team_event.ties, team_event.count)

        (
            team_event.qual_wins,
            team_event.qual_losses,
            team_event.qual_ties,
            team_event.qual_count,
        ) = te_qual_record[(team_event.team, team_event.event)]
        team_event.qual_winrate = winrate(
            team_event.qual_wins, team_event.qual_ties, team_event.qual_count
        )

        total_rps, count = te_rps[(team_event.team, team_event.event)]
        team_event.rps = total_rps
        team_event.rps_per_match = r(total_rps / max(1, count), 4)

    # Also handle event_obj num_teams, current_match, qual_matches
    event_to_team_events: Dict[str, List[TeamEvent]] = defaultdict(list)
    event_to_matches: Dict[str, List[Match]] = defaultdict(list)
    for team_event in objs[3].values():
        event_to_team_events[team_event.event].append(team_event)
    for match in objs[4].values():
        event_to_matches[match.event].append(match)

    for event in objs[2].values():
        event.num_teams = len(event_to_team_events[event.key])
        curr_matches = event_to_matches[event.key]
        event.current_match = len(
            [m for m in curr_matches if m.status == MatchStatus.COMPLETED]
        )
        event.qual_matches = len([m for m in curr_matches if not m.elim])

    # Also handles team_year_obj next_event_{key, name, week}
    team_to_events: Dict[int, List[Event]] = defaultdict(list)
    for event in objs[2].values():
        for team_event in event_to_team_events[event.key]:
            team_to_events[team_event.team].append(event)

    for team_year in objs[1].values():
        events = [
            e
            for e in team_to_events[team_year.team]
            if e.week >= CURR_WEEK and e.week != 9 and e.status != EventStatus.COMPLETED
        ]
        if len(events) > 0:
            next_event = min(events, key=lambda x: (x.week, x.num_teams))
            team_year.next_event_key = next_event.key
            team_year.next_event_name = next_event.name
            team_year.next_event_week = next_event.week

    return objs


def post_process(
    teams: List[Team], all_team_years: Dict[int, Dict[int, TeamYear]]
) -> List[Team]:
    t_record: Dict[int, TRecord] = defaultdict(lambda: (0, 0, 0, 0))
    t_active: Dict[int, bool] = defaultdict(lambda: False)

    all_team_years_list: List[TeamYear] = []
    for team_years_dict in all_team_years.values():
        all_team_years_list += list(team_years_dict.values())

    for team_year in all_team_years_list:
        team = team_year.team

        t_record[team] = (
            t_record[team][0] + team_year.wins,
            t_record[team][1] + team_year.losses,
            t_record[team][2] + team_year.ties,
            t_record[team][3] + team_year.count,
        )

        if team_year.year == CURR_YEAR:
            t_active[team] = True

    for team in teams:
        team.wins, team.losses, team.ties, team.count = t_record[team.team]
        team.winrate = winrate(team.wins, team.ties, team.count)

        team.active = t_active[team.team]

    return teams
