import matplotlib.pyplot as plt
from helper import utils

def getStats(year):
    matches = utils.loadProcessedMatches(year)
    error, true_preds = 0, 0

    for m in matches:
        error += (m.get_win_prob()-m.get_win_actual())**2
        if(m.correct_pred()): true_preds+=1

    mse = error/len(matches)
    acc = true_preds/len(matches)

    return [mse, acc]

def stats():
    total_mse = 0
    for year in range(2002, 2021):
        print(year)
        mse, acc = getStats(year)
        total_mse = total_mse+mse
        print("Brier: " + str(mse))
        print("Accuracy: " + str(acc))
        print()

    total_mse_sykes = 3.716 #see baseline
    print("Total mse ELO:  " + str(total_mse/19))
    print("Total mse Sykes: " + str(total_mse_sykes/19))

def mean():
    for year in range(2002, 2021):
        print(year)
        teams = utils.loadTeams(year)

        elos = []
        for team in teams.values():
            elos.append(team.get_rating())
        elos.sort()

        print("Elo Avg: " + str(sum(elos)/len(elos)))
        print("Elo 1%: " + str(elos[-int(len(elos)/100)]))
        #plt.hist(elos)
        #plt.show()

if __name__ == "__main__":
    stats()
    mean()
