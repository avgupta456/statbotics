from fastapi import APIRouter

from src.site.event import router as event_router
from src.site.match import router as match_router
from src.site.team import router as team_router
from src.site.team_year import router as team_year_router

router = APIRouter()
router.include_router(match_router, tags=["match"])
router.include_router(event_router, tags=["event"])
router.include_router(team_year_router, tags=["team_year"])
router.include_router(team_router, tags=["team"])


@router.get("/")
async def read_root():
    return {"name": "Site V3 Router"}
