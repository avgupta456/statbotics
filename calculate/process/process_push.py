import pandas as pd
from process.logging import printStats
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base


def getYears(SQL_Read):
    print("Years")
    years = []
    year_objs = SQL_Read.getYears()
    print(len(year_objs))
    for i, year in enumerate(year_objs):
        if i % 100000 == 0:
            print(i)
        years.append(
            [
                year.id,
                round(year.elo_acc, 4),
                round(year.elo_mse, 4),
                round(year.opr_acc, 4),
                round(year.opr_mse, 4),
                round(year.mix_acc, 4),
                round(year.mix_mse, 4),
                round(year.rp1_acc, 4),
                round(year.rp1_mse, 4),
                round(year.rp2_acc, 4),
                round(year.rp2_mse, 4),
                round(year.score_sd, 2),
                round(year.score_mean, 2),
            ]
        )

    years = pd.DataFrame(
        years,
        columns=[
            "year",
            "elo_acc",
            "elo_mse",
            "opr_acc",
            "opr_mse",
            "mix_acc",
            "mix_mse",
            "rp1_acc",
            "rp1_mse",
            "rp2_acc",
            "rp2_mse",
            "score_sd",
            "score_mean",
        ],
    )

    years = years.sort_values(by=["year"])
    return years


def getTeams(SQL_Read):
    print("Teams")
    teams = []
    team_objs = SQL_Read.getTeams()
    print(len(team_objs))
    for i, team in enumerate(team_objs):
        if i % 100000 == 0:
            print(i)
        teams.append(
            [
                team.id,
                team.name,
                team.state,
                team.country,
                team.district,
                team.active,
                round(team.elo),
                round(team.elo_recent),
                round(team.elo_mean),
                round(team.elo_max),
                team.wins,
                team.losses,
                team.ties,
                team.count,
                team.winrate,
            ]
        )

    teams = pd.DataFrame(
        teams,
        columns=[
            "team",
            "name",
            "state",
            "country",
            "district",
            "active",
            "elo",
            "elo_recent",
            "elo_mean",
            "elo_max",
            "wins",
            "losses",
            "ties",
            "count",
            "winrate",
        ],
    )

    teams = teams.sort_values(by=["team"])
    return teams


def getTeamYears(SQL_Read):
    print("Team Years")
    team_years = []
    team_year_objs = SQL_Read.getTeamYears()
    print(len(team_year_objs))
    for i, team_year in enumerate(team_year_objs):
        if i % 100000 == 0:
            print(i)
        team_years.append(
            [
                team_year.id,
                team_year.year_id,
                team_year.team_id,
                team_year.team.name,
                team_year.team.state,
                team_year.team.country,
                team_year.team.district,
                round(team_year.elo_start),
                round(team_year.elo_pre_champs),
                round(team_year.elo_end),
                round(team_year.elo_mean),
                round(team_year.elo_max),
                round(team_year.elo_diff),
                round(team_year.opr_end, 2),
                round(team_year.opr_auto, 2),
                round(team_year.opr_teleop, 2),
                round(team_year.opr_1, 2),
                round(team_year.opr_2, 2),
                round(team_year.opr_endgame, 2),
                round(team_year.opr_fouls, 2),
                round(team_year.opr_no_fouls, 2),
                round(team_year.ils_1, 2),
                round(team_year.ils_2, 2),
                team_year.wins,
                team_year.losses,
                team_year.ties,
                team_year.count,
                team_year.winrate,
                team_year.elo_rank,
                team_year.elo_percentile,
                team_year.opr_rank,
                team_year.opr_percentile,
            ]
        )

    team_years = pd.DataFrame(
        team_years,
        columns=[
            "id",
            "year",
            "team",
            "name",
            "state",
            "country",
            "district",
            "elo_start",
            "elo_pre_champs",
            "elo_end",
            "elo_mean",
            "elo_max",
            "elo_diff",
            "opr",
            "opr_auto",
            "opr_teleop",
            "opr_1",
            "opr_2",
            "opr_endgame",
            "opr_fouls",
            "opr_no_fouls",
            "ils_1",
            "ils_2",
            "wins",
            "losses",
            "ties",
            "count",
            "winrate",
            "elo_rank",
            "elo_percentile",
            "opr_rank",
            "opr_percentile",
        ],
    )

    team_years = team_years.sort_values(by=["year", "team"])
    return team_years


def getEvents(SQL_Read):
    print("Events")
    events = []
    event_objs = SQL_Read.getEvents()
    print(len(event_objs))
    for i, event in enumerate(event_objs):
        if i % 100000 == 0:
            print(i)
        events.append(
            [
                event.id,
                event.year_id,
                event.key,
                event.name,
                event.state,
                event.country,
                event.district,
                event.type,
                event.week,
                event.time,
                round(event.elo_top8),
                round(event.elo_top24),
                round(event.elo_mean),
                round(event.opr_top8, 2),
                round(event.opr_top24, 2),
                round(event.opr_mean, 2),
                event.elo_acc,
                event.elo_mse,
                event.opr_acc,
                event.opr_mse,
                event.mix_acc,
                event.mix_mse,
                event.rp1_acc,
                event.rp1_mse,
                event.rp2_acc,
                event.rp2_mse,
            ]
        )

    events = pd.DataFrame(
        events,
        columns=[
            "id",
            "year",
            "key",
            "name",
            "state",
            "country",
            "district",
            "type",
            "week",
            "time",
            "elo_top8",
            "elo_top24",
            "elo_mean",
            "opr_top8",
            "opr_top24",
            "opr_mean",
            "elo_acc",
            "elo_mse",
            "opr_acc",
            "opr_mse",
            "mix_acc",
            "mix_mse",
            "rp1_acc",
            "rp1_mse",
            "rp2_acc",
            "rp2_mse",
        ],
    )

    events = events.sort_values(by=["year", "key"])
    return events


def getTeamEvents(SQL_Read):
    print("Team Events")
    team_events = []
    team_event_objs = SQL_Read.getTeamEvents()
    print(len(team_event_objs))
    for i, team_event in enumerate(team_event_objs):
        if i % 100000 == 0:
            print(i)
        team_events.append(
            [
                team_event.id,
                team_event.team_id,
                team_event.team.name,
                team_event.year_id,
                team_event.event.key,
                team_event.event.state,
                team_event.event.country,
                team_event.event.district,
                team_event.event.type,
                team_event.event.week,
                team_event.event.time,
                round(team_event.elo_start),
                round(team_event.elo_pre_playoffs),
                round(team_event.elo_end),
                round(team_event.elo_mean),
                round(team_event.elo_max),
                round(team_event.elo_diff),
                round(team_event.opr_start, 2),
                round(team_event.opr_end, 2),
                round(team_event.opr_auto, 2),
                round(team_event.opr_teleop, 2),
                round(team_event.opr_1, 2),
                round(team_event.opr_2, 2),
                round(team_event.opr_endgame, 2),
                round(team_event.opr_fouls, 2),
                round(team_event.opr_no_fouls, 2),
                round(team_event.ils_1_start, 2),
                round(team_event.ils_2_start, 2),
                round(team_event.ils_1_end, 2),
                round(team_event.ils_2_end, 2),
            ]
        )

    team_events = pd.DataFrame(
        team_events,
        columns=[
            "id",
            "team",
            "name",
            "year",
            "event",
            "state",
            "country",
            "district",
            "type",
            "week",
            "time",
            "elo_start",
            "elo_pre_playoffs",
            "elo_end",
            "elo_mean",
            "elo_max",
            "elo_diff",
            "opr_start",
            "opr_end",
            "opr_auto",
            "opr_teleop",
            "opr_1",
            "opr_2",
            "opr_endgame",
            "opr_fouls",
            "opr_no_fouls",
            "ils_1_start",
            "ils_2_start",
            "ils_1_end",
            "ils_2_end",
        ],
    )

    team_events = team_events.sort_values(by=["year", "team", "event"])
    return team_events


def getMatches(SQL_Read):
    print("Matches")
    matches = []
    match_objs = SQL_Read.getMatches()
    print(len(match_objs))
    for i, match in enumerate(match_objs):
        if i % 100000 == 0:
            print(i)
        matches.append(
            [
                match.id,
                match.year_id,
                match.event.key,
                match.key,
                match.comp_level,
                match.set_number,
                match.match_number,
                match.playoff,
                match.time,
                match.red,
                match.blue,
                match.red_score,
                match.blue_score,
                match.winner,
                match.elo_winner,
                match.elo_win_prob,
                match.opr_winner,
                match.opr_win_prob,
                match.mix_winner,
                match.mix_win_prob,
                match.red_rp_1,
                match.red_rp_1_prob,
                match.red_rp_2,
                match.red_rp_2_prob,
                match.blue_rp_1,
                match.blue_rp_1_prob,
                match.blue_rp_2,
                match.blue_rp_2_prob,
                match.red_auto,
                match.blue_auto,
                match.red_teleop,
                match.blue_teleop,
                match.red_1,
                match.blue_1,
                match.red_2,
                match.blue_2,
                match.red_endgame,
                match.blue_endgame,
                match.red_fouls,
                match.blue_fouls,
                match.red_no_fouls,
                match.blue_no_fouls,
            ]
        )

    matches = pd.DataFrame(
        matches,
        columns=[
            "id",
            "year",
            "event",
            "key",
            "comp_level",
            "set_number",
            "match_number",
            "playoff",
            "time",
            "red",
            "blue",
            "red_score",
            "blue_score",
            "winner",
            "elo_winner",
            "elo_win_prob",
            "opr_winner",
            "opr_win_prob",
            "mix_winner",
            "mix_win_prob",
            "red_rp_1",
            "red_rp_1_prob",
            "red_rp_2",
            "red_rp_2_prob",
            "blue_rp_1",
            "blue_rp_1_prob",
            "blue_rp_2",
            "blue_rp_2_prob",
            "red_auto",
            "blue_auto",
            "red_teleop",
            "blue_teleop",
            "red_1",
            "blue_1",
            "red_2",
            "blue_2",
            "red_endgame",
            "blue_endgame",
            "red_fouls",
            "blue_fouls",
            "red_no_fouls",
            "blue_no_fouls",
        ],
    )

    matches = matches.sort_values(by=["year", "event", "key"])
    return matches


def getTeamMatches(SQL_Read):
    print("Team Matches")
    team_matches = []
    team_match_objs = SQL_Read.getTeamMatches()
    print(len(team_match_objs))
    for i, team_match in enumerate(team_match_objs):
        if i % 100000 == 0:
            print(i)
        team_matches.append(
            [
                team_match.id,
                team_match.team_id,
                team_match.year_id,
                team_match.event.key,
                team_match.match.key,
                team_match.match.playoff,
                team_match.alliance,
                team_match.match.time,
                team_match.elo,
                team_match.opr_score,
                team_match.ils_1,
                team_match.ils_2,
            ]
        )

    team_matches = pd.DataFrame(
        team_matches,
        columns=[
            "id",
            "team",
            "year",
            "event",
            "match",
            "playoff",
            "alliance",
            "time",
            "elo",
            "opr",
            "ils_1",
            "ils_2",
        ],
    )

    team_matches = team_matches.sort_values(by=["year", "team", "event", "match"])
    return team_matches


def pushClean(SQL_Read, cloud_engine):
    years = getYears(SQL_Read)
    years.to_sql("rankings_year", cloud_engine, if_exists="replace", index=False)

    teams = getTeams(SQL_Read)
    teams.to_sql("rankings_team", cloud_engine, if_exists="replace", index=False)

    teamYears = getTeamYears(SQL_Read)
    teamYears.to_sql(
        "rankings_teamyear", cloud_engine, if_exists="replace", index=False
    )

    events = getEvents(SQL_Read)
    events.to_sql("rankings_event", cloud_engine, if_exists="replace", index=False)

    teamEvents = getTeamEvents(SQL_Read)
    teamEvents.to_sql(
        "rankings_teamevent", cloud_engine, if_exists="replace", index=False
    )

    matches = getMatches(SQL_Read)
    matches.to_sql("rankings_match", cloud_engine, if_exists="replace", index=False)

    teamMatches = getTeamMatches(SQL_Read)
    teamMatches.to_sql(
        "rankings_teammatch", cloud_engine, if_exists="replace", index=False
    )

    printStats()


def drop_table(table_name, engine):
    base = declarative_base()
    metadata = MetaData(engine, reflect=True)
    table = metadata.tables.get(table_name)
    if table is not None:
        base.metadata.drop_all(engine, [table], checkfirst=True)


def main(SQL, SQL_Read):
    cloud_engine = SQL.getCloudEngine()
    # local_session = SQL.getLocalSession()
    pushClean(SQL_Read, cloud_engine)
    printStats()
