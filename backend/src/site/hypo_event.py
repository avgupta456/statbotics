# import random
# from typing import Any, Dict, List, Optional

# from src.site.aggregation import get_team_years, get_year, team_year_to_team_event
# from src.site.models import APIEvent, APIMatch, APITeamMatch, APITeamYear, APIYear
# from src.types.enums import MatchWinner
# from src.utils.hypothetical import decompress, get_cheesy_schedule

# TODO: Avoid code duplication with Database schema, EPA calculations, etc.

"""
async def read_hypothetical_event(
    event_id: str, no_cache: bool = False
) -> Dict[str, Any]:
    # TODO: allow decompress string teams
    year, teams, seed = decompress(event_id)

    event = APIEvent(
        key=event_id,
        name="Hypothetical Event",
        year=year,
        week=9,
        start_date=f"{year}-01-01",
        end_date=f"{year}-01-01",
        country=None,
        state=None,
        district=None,
        offseason=True,
        status="Upcoming",
        status_str="Upcoming",
        qual_matches=0,
        current_match=0,
        epa_acc=0,
        epa_mse=0,
        epa_max=0,
        epa_top_8=0,
        epa_top_24=0,
        epa_mean=0,
    )

    year_obj: Optional[APIYear] = await get_year(year=year, no_cache=no_cache)
    if year_obj is None:
        raise Exception("Year not found")

    team_years: List[APITeamYear] = await get_team_years(
        year=year, teams=[str(x) for x in teams], no_cache=no_cache
    )

    team_years_dict = {x.num: x for x in team_years}

    random.seed(seed)
    shuffled_teams = list([str(x) for x in teams])
    random.shuffle(shuffled_teams)
    schedule = get_cheesy_schedule(len(teams), 12)
    matches: List[APIMatch] = []
    team_matches: List[APITeamMatch] = []
    for i, x in enumerate(schedule):
        red_teams: List[str] = [shuffled_teams[x - 1] for x in x[:3]]
        red_team_objs: List[APITeamYear] = [team_years_dict[x] for x in red_teams]
        blue_teams: List[str] = [shuffled_teams[x - 1] for x in x[3:]]
        blue_team_objs: List[APITeamYear] = [team_years_dict[x] for x in blue_teams]
        red_epa_sum = sum([x.total_epa for x in red_team_objs])
        blue_epa_sum = sum([x.total_epa for x in blue_team_objs])
        win_prob = 1 / (
            1 + 10 ** (-5 / 8 * (red_epa_sum - blue_epa_sum) / year_obj.score_sd)
        )
        matches.append(
            APIMatch(
                key=f"{event_id}_qm{i+1}",
                year=year,
                event=event_id,
                time=0,
                predicted_time=0,
                match_name=f"Qualification {i+1}",
                status="Upcoming",
                video=None,
                comp_level="qm",
                set_number=0,
                match_number=i + 1,
                elim=False,
                red=red_teams,
                blue=blue_teams,
                red_surrogates=[],
                blue_surrogates=[],
                red_dqs=[],
                blue_dqs=[],
                red_score=0,
                blue_score=0,
                red_rp_1=0,
                red_rp_2=0,
                blue_rp_1=0,
                blue_rp_2=0,
                red_tiebreaker=0,
                blue_tiebreaker=0,
                winner="",
                red_epa_pred=sum(x.total_epa for x in red_team_objs),
                blue_epa_pred=sum(x.total_epa for x in blue_team_objs),
                epa_win_prob=win_prob,
                pred_winner=MatchWinner.RED if win_prob > 0.5 else MatchWinner.BLUE,
            )
        )

        for team in red_teams + blue_teams:
            team_matches.append(
                APITeamMatch(
                    alliance=MatchWinner.RED if team in red_teams else MatchWinner.BLUE,
                    num=team,
                    match=f"{event_id}_qm{i+1}",
                    time=0,
                    status="Upcoming",
                    elim=False,
                    match_number=i + 1,
                    total_epa=team_years_dict[team].total_epa,
                    auto_epa=team_years_dict[team].auto_epa,
                    teleop_epa=team_years_dict[team].teleop_epa,
                    endgame_epa=team_years_dict[team].endgame_epa,
                    rp_1_epa=team_years_dict[team].rp_1_epa,
                    rp_2_epa=team_years_dict[team].rp_2_epa,
                    post_epa=team_years_dict[team].total_epa,
                    offseason=True,
                )
            )

    return {
        "event": event.to_dict(),
        "matches": [x.to_dict() for x in matches],
        "team_events": [
            team_year_to_team_event(x, event).to_dict() for x in team_years
        ],
        "team_matches": [x.to_dict() for x in team_matches],
        "year": year_obj.to_dict(),
    }
"""
