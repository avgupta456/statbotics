from fastapi import APIRouter


from src.db.read.year import get_num_years
from src.db.read.team import get_num_teams
from src.db.read.event import get_num_events
from src.db.read.match import get_num_matches
from src.db.read.team_year import get_num_team_years
from src.db.read.team_event import get_num_team_events
from src.db.read.team_match import get_num_team_matches

router = APIRouter()


@router.get("/")
async def read_root():
    return {
        "years": get_num_years(),
        "teams": get_num_teams(),
        "events": get_num_events(),
        "matches": get_num_matches(),
        "team_years": get_num_team_years(),
        "team_events": get_num_team_events(),
        "team_matches": get_num_team_matches(),
    }
