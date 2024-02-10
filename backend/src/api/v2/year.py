from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Response

from src.api.year import get_year_cached, get_years_cached
from src.db.models import Year
from src.utils.decorators import (
    async_fail_gracefully_plural,
    async_fail_gracefully_singular,
)

router = APIRouter()


def get_v2_year(year: Year) -> Dict[str, Any]:
    return {
        "year": year.year,
        "epa_max": None,
        "epa_1p": year.epa_99p,
        "epa_5p": None,
        "epa_10p": year.epa_90p,
        "epa_25p": year.epa_75p,
        "epa_median": None,
        "epa_75p": year.epa_25p,
        "epa_mean": None,
        "epa_sd": None,
        "auto_epa_max": None,
        "auto_epa_1p": year.auto_epa_99p,
        "auto_epa_5p": None,
        "auto_epa_10p": year.auto_epa_90p,
        "auto_epa_25p": year.auto_epa_75p,
        "auto_epa_median": None,
        "auto_epa_75p": year.auto_epa_25p,
        "auto_epa_mean": None,
        "auto_epa_sd": None,
        "teleop_epa_max": None,
        "teleop_epa_1p": year.teleop_epa_99p,
        "teleop_epa_5p": None,
        "teleop_epa_10p": year.teleop_epa_90p,
        "teleop_epa_25p": year.teleop_epa_75p,
        "teleop_epa_median": None,
        "teleop_epa_75p": year.teleop_epa_25p,
        "teleop_epa_mean": None,
        "teleop_epa_sd": None,
        "endgame_epa_max": None,
        "endgame_epa_1p": year.endgame_epa_99p,
        "endgame_epa_5p": None,
        "endgame_epa_10p": year.endgame_epa_90p,
        "endgame_epa_25p": year.endgame_epa_75p,
        "endgame_epa_median": None,
        "endgame_epa_75p": year.endgame_epa_25p,
        "endgame_epa_mean": None,
        "endgame_epa_sd": None,
        "rp_1_epa_max": None,
        "rp_1_epa_1p": year.rp_1_epa_99p,
        "rp_1_epa_5p": None,
        "rp_1_epa_10p": year.rp_1_epa_90p,
        "rp_1_epa_25p": year.rp_1_epa_75p,
        "rp_1_epa_median": None,
        "rp_1_epa_75p": year.rp_1_epa_25p,
        "rp_1_epa_mean": None,
        "rp_1_epa_sd": None,
        "rp_2_epa_max": None,
        "rp_2_epa_1p": year.rp_2_epa_99p,
        "rp_2_epa_5p": None,
        "rp_2_epa_10p": year.rp_2_epa_90p,
        "rp_2_epa_25p": year.rp_2_epa_75p,
        "rp_2_epa_median": None,
        "rp_2_epa_75p": year.rp_2_epa_25p,
        "rp_2_epa_mean": None,
        "rp_2_epa_sd": None,
        "epa_quals_acc": None,
        "epa_quals_mse": None,
        "quals_count": None,
        "epa_elims_acc": None,
        "epa_elims_mse": None,
        "elims_count": None,
        "epa_champs_acc": year.epa_champs_acc,
        "epa_champs_mse": year.epa_champs_mse,
        "champs_count": year.champs_count,
        "epa_acc": year.epa_acc,
        "epa_mse": year.epa_mse,
        "count": year.count,
        "rp_1_acc": year.epa_rp_1_acc,
        "rp_1_mse": None,
        "rp_1_champs_acc": year.epa_champs_rp_1_acc,
        "rp_1_champs_mse": None,
        "rp_2_acc": year.epa_rp_2_acc,
        "rp_2_mse": None,
        "rp_2_champs_acc": year.epa_champs_rp_2_acc,
        "rp_2_champs_mse": None,
        "rp_champs_count": year.champs_rp_count,
        "rp_count": year.rp_count,
        "score_mean": year.score_mean,
        "score_sd": year.score_sd,
        "auto_mean": year.auto_mean,
        "teleop_mean": year.teleop_mean,
        "endgame_mean": year.endgame_mean,
        "fouls_mean": year.foul_mean,
        "no_fouls_mean": year.no_foul_mean,
        "rp_1_mean": year.rp_1_mean,
        "rp_2_mean": year.rp_2_mean,
    }


@router.get("/")
async def read_root_year():
    return {"name": "Year Router"}


@router.get(
    "/year/{year}",
    description="Get a single Year object containing EPA percentiles, Week 1 match score statistics, and prediction accuracy. After 2016, separated into components and ranking points included.",
    response_description="A Year object.",
)
@async_fail_gracefully_singular
async def read_year(
    response: Response,
    year: int,
) -> Dict[str, Any]:
    year_obj: Optional[Year] = await get_year_cached(year=year)
    if year_obj is None:
        raise Exception("Year not found")

    return get_v2_year(year_obj)


@router.get(
    "/years",
    description="Get a list of Year objects from 2002 to 2023. Specify a four-digit year, ex: 2019",
    response_description="A list of Year objects. See /year/{year} for more information.",
)
@async_fail_gracefully_plural
async def read_years(
    response: Response,
    metric: Optional[str] = None,
    ascending: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Dict[str, Any]]:
    years: List[Year] = await get_years_cached(
        metric=metric, ascending=ascending, limit=limit, offset=offset
    )
    return [get_v2_year(year) for year in years]
