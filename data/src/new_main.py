from dotenv import load_dotenv

load_dotenv()

from db.read.event import get_num_events as get_num_events_db
from db.read.match import get_num_matches as get_num_matches_db
from db.read.team import get_num_teams as get_num_teams_db
from db.read.team_event import get_num_team_events as get_num_team_events_db
from db.read.team_match import get_num_team_matches
from db.read.team_year import get_num_team_years as get_num_team_years_db
from db.read.year import get_num_years as get_num_years_db

# from new_process.process_avg import main as process_avg
# from new_process.process_elo import main as process_elo
from new_process.process_opr import main as process_opr

# from new_process.process_tba import main as process_tba


def print_table_stats() -> None:
    print("Num Teams:", get_num_teams_db())
    print("Num Years:", get_num_years_db())
    print("Num Team Years:", get_num_team_years_db())
    print("Num Events:", get_num_events_db())
    print("Num Team Events:", get_num_team_events_db())
    print("Num Matches:", get_num_matches_db())
    print("Num Team Matches:", get_num_team_matches())


start_year = 2002
end_year = 2020


# print("PROCESS TBA")
# process_tba(start_year, end_year, cache=True)
# process_avg(start_year, end_year)
# print("PROCESS ELO")
# process_elo(start_year, end_year)
print("PROCESS OPR")
process_opr(start_year, end_year)
print()
print_table_stats()

print("Done!")
