import matplotlib.pyplot as plt
import utils

def getStats(year):
    matches = utils.loadProcessedMatches(year)
    print(len(matches))

    error_ts, true_preds_ts = 0, 0
    error_elo, true_preds_elo = 0, 0

    for m in matches:
        error_ts += (m.get_win_prob_ts()-m.get_win_actual())**2
        if(m.correct_pred_ts()): true_preds_ts+=1

        error_elo += (m.get_win_prob_elo()-m.get_win_actual())**2
        if(m.correct_pred_elo()): true_preds_elo+=1

    mse_ts = error_ts/len(matches)
    acc_ts = true_preds_ts/len(matches)

    mse_elo = error_elo/len(matches)
    acc_elo = true_preds_elo/len(matches)

    return [mse_ts, acc_ts, mse_elo, acc_elo]

def stats():
    total_mse_ts, total_mse_elo = 0, 0
    for year in range(2010, 2021):
        print(year)
        mse_ts, acc_ts, mse_elo, acc_elo = getStats(year)
        total_mse_ts, total_mse_elo = total_mse_ts+mse_ts, total_mse_elo+mse_elo
        print("Trueskill")
        print("Brier: " + str(mse_ts))
        print("Accuracy: " + str(acc_ts))
        print("Elo")
        print("Brier: " + str(mse_elo))
        print("Accuracy: " + str(acc_elo))
        print()

    total_mse_sykes = 1.838
    print("Total mse ELO:  " + str(total_mse_elo/10))
    print("Total mse TS:   " + str(total_mse_ts/10))
    print("Total mse Sykes: " + str(total_mse_sykes/10))


def mean():
    for year in range(2010, 2021):
        print(year)
        teams = utils.loadTeams(year)
        elos, tss = [], []
        for team in teams.values():
            elos.append(team.get_rating_elo())
            tss.append(team.get_rating_ts())

        elos.sort()
        tss.sort()

        print("Elo Avg: " + str(sum(elos)/len(elos)))
        print("Ts Avg:  " + str(sum(tss)/len(tss)))
        print("Elo 1%: " + str(elos[-int(len(elos)/100)]))
        print("Ts 1%:  " + str(tss[-int(len(tss)/100)]))
        #plt.hist([elos, tss])
        #plt.show()

if __name__ == "__main__":
    stats()
    #mean()
