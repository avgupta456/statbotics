from fastapi import APIRouter

from src.data.insert.main import process_main

router = APIRouter()


@router.get("/")
async def read_root():
    return {"name": "Data Router"}


@router.get("/reset")
async def reset():
    process_main(start_year=2002, end_year=2022, clean=True)
    return {"status": "success"}
