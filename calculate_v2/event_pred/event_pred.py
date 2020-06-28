from helper import setup
from models import opr

clean = False
TBA, SQL, SQL_Read, SQL_Write = setup.setup(clean)

# your code here
event = SQL_Read.getEvent_byKey('2016arc')
teams = []
for team_event in event.team_events:
    teams.append(team_event.team_id)
oprs, ils = opr.opr_standalone(SQL_Read, event)
teams = oprs.keys()

quals = sorted(SQL_Read.getMatches(event=event.id, playoff=False))
playoffs = sorted(SQL_Read.getMatches(event=event.id, playoff=True))
