from fastapi import Query

from src.constants import CURR_YEAR

active_query = Query(None, description="Whether the team has played in the last year.")

ascending_query = Query(
    None,
    description="Whether to sort the returned values in ascending order. Default is ascending",
)

country_query = Query(
    None, description="Capitalized country name, e.g. `USA` or `Canada`."
)

district_query = Query(
    None,
    description="One of [`fma`, `fnc`, `fsc`, `fit`, `fin`, `fim`, `ne`, `chs`, `ont`, `pnw`, `pch`, `isr`]",
)

elim_query = Query(None, description="Whether the match is an elimination match.")

event_query = Query(None, description="Event key, e.g. `2019ncwak`.")

event_type_query = Query(
    None,
    description="One of [`regional`, `district`, `district_cmp`, `cmp_division`, or `cmp_finals`].",
)

limit_query = Query(
    None,
    ge=1,
    le=1000,
    description="Maximum number of events to return. Default is 1000.",
)

match_query = Query(None, description="Match key, e.g. `2019ncwak_f1m1`.")

metric_query = Query(
    None,
    description="How to sort the returned values. Any column in the table is valid.",
)

offset_query = Query(None, ge=0, description="Offset from the first result to return.")
state_query = Query(None, description="Capitalized two-letter state code, e.g. `NC`.")

team_query = Query(
    None, ge=0, lt=100000, description="Team number (no prefix), e.g. 5511."
)

week_query = Query(
    None, ge=0, le=8, description="Week of the competition season. 8 is CMP"
)

year_query = Query(None, ge=2002, le=CURR_YEAR, description="Four-digit year")
