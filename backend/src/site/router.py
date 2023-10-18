from fastapi import APIRouter

from src.constants import CURR_YEAR, MAX_YEAR
from src.data.main import reset_curr_year, update_curr_year
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
    return {"name": "Site Router"}


# To reduce cost in the offseason, update data through the site router


@router.get("/reset_curr_year")
async def reset_curr_year_endpoint():
    for year in range(CURR_YEAR, MAX_YEAR + 1):
        reset_curr_year(curr_year=year)
    return {"status": "success"}


@router.get("/update_curr_year")
async def update_curr_year_endpoint():
    update_curr_year(curr_year=CURR_YEAR)
    return {"status": "success"}
