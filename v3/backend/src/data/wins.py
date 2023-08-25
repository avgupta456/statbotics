from collections import defaultdict
from typing import List, Dict, Tuple

from src.data.utils import objs_type
from src.db.models import Team, TeamYear
from src.constants import CURR_YEAR


def winrate(wins: int, ties: int, count: int) -> float:
    return round((wins + ties / 2) / max(1, count), 4)


TRecord = Tuple[int, int, int, int]


def process_year(objs: objs_type) -> objs_type:
    year_num = objs[0].year

    ty_record: Dict[str, TRecord] = defaultdict(lambda: (0, 0, 0, 0))
    ty_full_record: Dict[str, TRecord] = defaultdict(lambda: (0, 0, 0, 0))
    te_record: Dict[Tuple[str, str], TRecord] = defaultdict(lambda: (0, 0, 0, 0))
    te_qual_record: Dict[Tuple[str, str], TRecord] = defaultdict(lambda: (0, 0, 0, 0))
    te_rps: Dict[Tuple[str, str], Tuple[int, int]] = defaultdict(lambda: (0, 0))

    for a_obj in objs[5].values():
        elim = a_obj.elim
        event = a_obj.event
        status = a_obj.status
        alliance = a_obj.alliance
        offseason = a_obj.offseason
        winner = a_obj.official_winner

        if status != "Completed" or winner is None:
            continue

        win_update = 1 if alliance == winner else 0
        tie_update = 1 if winner == "tie" else 0
        loss_update = 1 - win_update - tie_update

        rp_1 = a_obj.rp_1 or 0
        rp_2 = a_obj.rp_2 or 0
        total_rps = 2 * win_update + 1 * tie_update + rp_1 + rp_2

        update = (win_update, loss_update, tie_update, 1)
        rp_update = (total_rps, 1)

        teams = [a_obj.team_1, a_obj.team_2, a_obj.team_3]
        dqs = a_obj.dq.split(",")
        surrogates = a_obj.surrogate.split(",")

        if year_num <= 2004:
            teams = teams[:2]  # 2 team alliances

        for t in teams:
            if t is None:
                continue

            ty_full_record[t] = tuple(sum(x) for x in zip(ty_full_record[t], update))

            if not offseason:
                ty_record[t] = tuple(sum(x) for x in zip(ty_record[t], update))

            if t not in dqs and t not in surrogates:
                # DQ, surrogate only affect TeamEvent records
                te_record[(t, event)] = tuple(
                    sum(x) for x in zip(te_record[(t, event)], update)
                )
                if not elim:
                    te_qual_record[(t, event)] = tuple(
                        sum(x) for x in zip(te_qual_record[(t, event)], update)
                    )
                    te_rps[(t, event)] = tuple(
                        sum(x) for x in zip(te_rps[(t, event)], rp_update)
                    )

    for team_year in objs[1].values():
        (
            team_year.wins,
            team_year.losses,
            team_year.ties,
            team_year.count,
        ) = ty_record[team_year.team]
        team_year.winrate = winrate(team_year.wins, team_year.ties, team_year.count)

        (
            team_year.full_wins,
            team_year.full_losses,
            team_year.full_ties,
            team_year.full_count,
        ) = ty_full_record[team_year.team]
        team_year.full_winrate = winrate(
            team_year.full_wins, team_year.full_ties, team_year.full_count
        )

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
        team_event.rps_per_match = round(total_rps / max(1, count), 4)

    return objs


def post_process(teams: List[Team], all_team_years: List[TeamYear]) -> List[Team]:
    t_record: Dict[str, TRecord] = defaultdict(lambda: (0, 0, 0, 0))
    t_full_record: Dict[str, TRecord] = defaultdict(lambda: (0, 0, 0, 0))
    t_active: Dict[str, bool] = defaultdict(lambda: False)

    for team_year in all_team_years:
        team = team_year.team

        update = (team_year.wins, team_year.losses, team_year.ties, team_year.count)
        t_record[team] = tuple(sum(x) for x in zip(t_record[team], update))

        full_update = (
            team_year.full_wins,
            team_year.full_losses,
            team_year.full_ties,
            team_year.full_count,
        )
        t_full_record[team] = tuple(
            sum(x) for x in zip(t_full_record[team], full_update)
        )

        if team_year.year == CURR_YEAR:
            t_active[team] = True

    for team in teams:
        team.wins, team.losses, team.ties, team.count = t_record[team.team]
        team.winrate = winrate(team.wins, team.ties, team.count)

        (
            team.full_wins,
            team.full_losses,
            team.full_ties,
            team.full_count,
        ) = t_full_record[team.team]
        team.full_winrate = winrate(team.full_wins, team.full_ties, team.full_count)

        team.active = t_active[team.team]

    return teams
