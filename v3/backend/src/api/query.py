from fastapi import Query

alliance_query = Query(None, description="Alliance color, e.g. `red` or `blue`.")

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
    description="One of [`fma`, `fnc`, `fit`, `fin`, `fim`, `ne`, `chs`, `ont`, `pnw`, `pch`, `isr`]",
)

elim_query = Query(None, description="Whether the match is an elimination match.")

event_query = Query(None, description="Event key, e.g. `2019ncwak`.")

event_type_query = Query(
    None,
    description="One of [`regional`, `district`, `district_cmp`, `cmp_division`, `cmp_finals`, `offseason`, or `preseason`].",
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

offseason_query = Query(None, description="Whether the event is an offseason event.")

offset_query = Query(None, ge=0, description="Offset from the first result to return.")
state_query = Query(None, description="Capitalized two-letter state code, e.g. `NC`.")

team_query = Query(
    None, ge=0, le=99999, description="Team number (no prefix), e.g. `5511`."
)

week_query = Query(
    None,
    ge=0,
    le=9,
    description="Week of the competition season. 0 is preseason, 8 is CMP, 9 is offseason.",
)

year_query = Query(None, ge=2002, le=2024, description="Four-digit year")
