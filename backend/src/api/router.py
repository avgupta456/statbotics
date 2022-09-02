from fastapi import APIRouter

from src.api.stats import router as stats_router


router = APIRouter()


@router.get("/")
async def read_root():
    return {"name": "API Router"}


router.include_router(stats_router, prefix="/stats")
