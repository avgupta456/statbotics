from fastapi import APIRouter

from src.api.v2.event import router as event_router
from src.api.v2.match import router as match_router
from src.api.v2.team import router as team_router
from src.api.v2.team_event import router as team_event_router
from src.api.v2.team_match import router as team_match_router
from src.api.v2.team_year import router as team_year_router
from src.api.v2.year import router as year_router

router = APIRouter()
router.include_router(year_router, tags=["v2/Year"])
router.include_router(team_router, tags=["v2/Team"])
router.include_router(team_year_router, tags=["v2/TeamYear"])
router.include_router(event_router, tags=["v2/Event"])
router.include_router(team_event_router, tags=["v2/TeamEvent"])
router.include_router(match_router, tags=["v2/Match"])
router.include_router(team_match_router, tags=["v2/TeamMatch"])


@router.get("/")
async def read_root():
    return {"name": "API V2 Router"}
