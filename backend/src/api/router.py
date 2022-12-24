from fastapi import APIRouter

from src.api.event import router as event_router
from src.api.match import router as match_router
from src.api.team_year import router as team_year_router

router = APIRouter()
router.include_router(match_router, prefix="/match", tags=["match"])
router.include_router(event_router, prefix="/event", tags=["event"])
router.include_router(team_year_router, prefix="/team_year", tags=["team_year"])


@router.get("/")
async def read_root():
    return {"name": "API Router"}
