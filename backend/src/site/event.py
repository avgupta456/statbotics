from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Response

from src.utils.compress import compress, decompress
from src.site.aggregation import (
    get_event,
    get_events,
    get_matches,
    get_team_events,
    get_team_matches,
    get_team_years,
    get_year,
    team_year_to_team_event,
)
from src.site.models import (
    APIEvent,
    APIMatch,
    APITeamEvent,
    APITeamMatch,
    APITeamYear,
    APIYear,
)
from src.utils.decorators import async_fail_gracefully

router = APIRouter()


@router.get("/events/all")
@async_fail_gracefully
async def read_all_events(response: Response) -> List[Dict[str, Any]]:
    events: List[APIEvent] = await get_events()
    return [{"key": event.key, "name": event.name} for event in events]


@router.get("/events/{year}")
@async_fail_gracefully
async def read_events(response: Response, year: int) -> Dict[str, Any]:
    year_obj: Optional[APIYear] = await get_year(year=year)
    if year_obj is None:
        raise Exception("Year not found")

    events: List[APIEvent] = await get_events(year=year, offseason=None)
    return {"year": year_obj.to_dict(), "events": [x.to_dict() for x in events]}


@router.get("/event/{event_id}")
@async_fail_gracefully
async def read_event(response: Response, event_id: str) -> Dict[str, Any]:
    event: Optional[APIEvent] = await get_event(event=event_id)
    if event is None:
        raise Exception("Event not found")

    year: Optional[APIYear] = await get_year(year=event.year)
    if year is None:
        raise Exception("Year not found")

    team_events: List[APITeamEvent] = await get_team_events(
        year=year.year,
        score_mean=year.score_mean / (1 + year.foul_rate),
        score_sd=year.score_sd,
        event=event_id,
        offseason=event.offseason,
    )
    matches: List[APIMatch] = await get_matches(
        event=event_id, offseason=event.offseason
    )
    team_matches: List[APITeamMatch] = await get_team_matches(
        event=event_id, offseason=event.offseason
    )

    out = {
        "event": event.to_dict(),
        "matches": [x.to_dict() for x in matches],
        "team_events": [x.to_dict() for x in team_events],
        "team_matches": [x.to_dict() for x in team_matches],
        "year": year.to_dict(),
    }

    return out


@router.get("/event/hypothetical/test_compression")
@async_fail_gracefully
async def test_compression(response: Response) -> bool:
    test = decompress(compress(2023, [254, 1323, 1678], 10))

    out = True

    if test[0] != 2023:
        print("year")
        out = False

    if len(test[1]) != 3:
        print("teams")
        out = False

    if 254 not in test[1]:
        print("254")
        out = False

    if 1323 not in test[1]:
        print("1323")
        out = False

    if 1678 not in test[1]:
        print("1678")
        out = False

    if test[2] != 10:
        print("match")
        out = False

    return out


@router.get("/event/hypothetical/{event_id}")
@async_fail_gracefully
async def read_hypothetical_event(response: Response, event_id: str) -> Dict[str, Any]:
    year, teams, _ = decompress(event_id)

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
        epa_top8=0,
        epa_top24=0,
        epa_mean=0,
    )

    year_obj: Optional[APIYear] = await get_year(year=year)
    if year_obj is None:
        raise Exception("Year not found")

    team_years: List[APITeamYear] = await get_team_years(
        year=year, teams=frozenset(teams)
    )

    return {
        "event": event.to_dict(),
        "matches": [],
        "team_events": [
            team_year_to_team_event(x, event).to_dict() for x in team_years
        ],
        "team_matches": [],
        "year": year_obj.to_dict(),
    }


@router.get("/event/{event_id}/team_matches/{team}")
@async_fail_gracefully
async def read_team_matches(
    response: Response, event_id: str, team: int
) -> List[Dict[str, Any]]:
    team_matches: List[APITeamMatch] = await get_team_matches(event=event_id, team=team)
    return [x.to_dict() for x in team_matches]
