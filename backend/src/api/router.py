from fastapi import APIRouter

from src.api.year import router as year_router

router = APIRouter()
router.include_router(year_router, tags=["Year"])


@router.get("/")
async def read_root():
    return {"name": "API Router"}
