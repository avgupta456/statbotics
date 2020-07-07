import datetime

import helper.setup as setup
import event_pred.event_pred as event_pred

start = datetime.datetime.now()
TBA, SQL, SQL_Read, SQL_Write = setup.setup_cloud(clean=False)
stop1 = datetime.datetime.now()
print("Load")
print(stop1-start)

year = 2019
event_key = 'nccmp'
index = 10

out = event_pred.sim(SQL_Read, year, event_key)
for team in out.keys():
    print(team, round(out[team][index][0], 2), round(out[team][index][1], 2))
print()

stop2 = datetime.datetime.now()
print(stop2-stop1)
print("Event Sim")
