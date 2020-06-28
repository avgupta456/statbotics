from helper import setup, utils
from models import opr as opr_model
from models import elo as elo_model
from event_pred import rps as rps_model

TBA, SQL, SQL_Read, SQL_Write = setup.setup(False)
print("Finished Setup")

# your code here
year = 2016
event = 'arc'

event = SQL_Read.getEvent_byKey(str(year)+event)
sd_score = event.year.score_sd
teams = []
for team_event in event.team_events:
    teams.append(team_event.team_id)

quals = sorted(SQL_Read.getMatches(event=event.id, playoff=False))
playoffs = sorted(SQL_Read.getMatches(event=event.id, playoff=True))
oprs, ils = opr_model.opr_v2(event, quals, playoffs)
elos = elo_model.get_elos(event, quals)
rps = rps_model.get_rps(event, quals)
teams = oprs.keys()

index = 50
oprs_ind, ils_ind, rps_ind = {}, {}, {}
for team in teams:
    oprs_ind[team] = oprs[team][index]
    ils_ind[team] = ils[team][index]
    rps_ind[team] = rps[team][index]

preds = {}  # for each match i, win_prob, red_rp1, red_rp2, blue_rp1, blue_rp2
for i in range(index+1, len(quals)):
    m = quals[i]
    red, blue = m.getTeams()
    red_score = sum([utils.clean(oprs_ind[t][0]) for t in red])
    blue_score = sum([utils.clean(oprs_ind[t][0]) for t in blue])
    red_elo = sum([utils.clean(elos[t][0]) for t in red])
    blue_elo = sum([utils.clean(elos[t][0]) for t in blue])

    elo_prob = elo_model.win_prob(red_elo, blue_elo)
    elo_margin = elo_model.win_margin(red_elo, blue_elo, sd_score)
    opr_prob = opr_model.win_prob(red_score, blue_score, year, sd_score)
    win_prob = (elo_prob + opr_prob)/2
    win_margin = (elo_margin + (red_score - blue_score))/2
    red_score = (red_score + blue_score)/2 + win_margin/2
    blue_score = (red_score + blue_score)/2 - win_margin/2

    red_rp_1 = opr_model.rp_prob([ils_ind[t][0] for t in red])
    red_rp_2 = opr_model.rp_prob([ils_ind[t][1] for t in red])
    blue_rp_1 = opr_model.rp_prob([ils_ind[t][0] for t in blue])
    blue_rp_2 = opr_model.rp_prob([ils_ind[t][1] for t in blue])

    preds[i] = [round(red_score), round(blue_score), round(win_prob, 2),
                round(red_rp_1, 2), round(red_rp_2, 2),
                round(blue_rp_1, 2), round(blue_rp_2, 2)]

for i in range(index+1, len(quals)):
    print("Predicting Match", i+1)
    print("Score:", preds[i][0], preds[i][1])
    print("Red Win Prob:", preds[i][2])
    print("Red RP Probs:", preds[i][3], preds[i][4])
    print("Blue RP Probs:", preds[i][5], preds[i][6])
    print()
