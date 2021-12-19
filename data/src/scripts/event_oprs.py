from helper import setup
from process import process_opr

start_year = 2002
end_year = 2020
clean = False

TBA, SQL, SQL_Read, SQL_Write = setup.setup(clean)

year = 2017
year_obj = SQL_Read.getYear(year)
sd_score = year_obj.score_sd

events = SQL_Read.getEvents(year=year)
event = events[0]

quals = SQL_Read.getMatches(event=event.getId(), playoff=False)
playoffs = SQL_Read.getMatches(event=event.getId(), playoff=True)
oprs, stats = process_opr.process_event(event, quals, playoffs, year, sd_score)
for team in oprs:
    print(team, oprs[team][-1][0])
print(len(oprs[team]))
print(len(quals))
