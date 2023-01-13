from fastapi import APIRouter

from src.api.event import router as event_router
from src.api.team_year import router as team_year_router
from src.api.team import router as team_router
from src.api.year import router as year_router

router = APIRouter()
router.include_router(year_router, tags=["Year"])
router.include_router(team_router, tags=["Team"])
router.include_router(team_year_router, tags=["TeamYear"])
router.include_router(event_router, tags=["Event"])


@router.get("/")
async def read_root():
    return {"name": "API Router"}
