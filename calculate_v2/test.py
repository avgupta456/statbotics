from classes import (
    sql,
    read,
    write
)

from tba import (
    read_tba,
)

from models import (
    opr as opr_model,
)

from scripts import (
    process_opr,
)

start_year = 2002
end_year = 2020
clean = False

TBA = read_tba.ReadTBA()
SQL = sql.SQL(clean=clean, echo=False)
SQL_Read = read.SQL_Read(SQL)
SQL_Write = write.SQL_Write(SQL, SQL_Read)

year = 2017
year_obj = SQL_Read.getYear(year)
sd_score = year_obj.score_sd

events = SQL_Read.getEvents(year=year)
for event in events[:1]:
    quals = SQL_Read.getMatches(event=event.getId(), playoff=False)
    playoffs = SQL_Read.getMatches(event=event.getId(), playoff=True)
    test, oprs, stats = process_opr.process_event(event, quals, playoffs, year, sd_score)
    for team in oprs:
        print(team, oprs[team][-1][0], test[team][-1][0])
    print(len(oprs[team]))
    print(len(quals))
