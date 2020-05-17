import utils
import argparse
import elo

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--action', type=str, help='action', default='lookup', required=True)
    parser.add_argument('-m', '--metric', type=str, help='elo or ts', default='ts', required=False)
    parser.add_argument('-t', '--team', type=int, help="team", required=False)
    parser.add_argument('-y', '--year', type=str, help="year", required=True)
    parser.add_argument('-y2', '--year2', type=str, help="year2", required=False)
    return parser.parse_args()

def lookup(year, team, metric):
    teams = utils.loadTeams(year)
    team = teams[team]

    ratings = team.ratings_elo
    if(metric=="ts"): ratings = team.ratings_ts

    rating = team.get_rating_max_elo()
    if(metric=="ts"): rating = team.get_rating_max_ts()

    for i in range(len(ratings)):
        print(str(i+1)+":\t"+str(ratings[i]))
    print("Max:   " + str(rating))

def leaderboard(year, rating):
    teams = utils.loadTeams(year)
    board = sorted(teams.values())[:25]
    for i in range(len(board)):
        if(rating=="elo"): print(str(i+1)+"\t"+str(board[i].number)+"\t"+str(board[i].get_rating_max_elo()))
        else: print(str(i+1)+"\t"+str(board[i].number)+"\t"+str(board[i].get_rating_max_ts()))

def rank(year, team, metric, print=True):
    teams = utils.loadTeams(year)
    num_teams = len(teams)

    if(metric=="elo"):
        elos = []
        for t in teams.values(): elos.append(t.get_rating_max_elo())
        elos.sort()

        elo_rank = num_teams-elos.index(teams[team].get_rating_max_elo())
        elo_percent = int(1000*elo_rank/num_teams)/10

        if(print): print("Elo Rank:\t" + str(elo_rank) + "\t(Top " + str(elo_percent) + "%)")
        return elo_rank

    else:
        tss = []
        for t in teams.values(): tss.append(t.get_rating_max_ts())
        tss.sort()

        ts_rank = num_teams-tss.index(teams[team].get_rating_max_ts())
        ts_percent = int(1000*ts_rank/num_teams)/10

        if(print): print("TS Rank:\t" + str(ts_rank) + "\t(Top " + str(ts_percent) + "%)")
        return ts_rank

def ranks(start_year, end_year, team, metric):
    for year in range(int(start_year), int(end_year)+1):
        print(str(year)+"\t"+str(rank(year, team, metric, False))+"/"+str(len(utils.loadTeams(year))))

if __name__ == "__main__":
    args = get_args()
    if(args.action=="lookup"): lookup(args.year, args.team, args.metric)
    elif(args.action=="leaderboard"): leaderboard(args.year, args.metric)
    elif(args.action=="rank"): rank(args.year, args.team)
    elif(args.action=="ranks"): ranks(args.year, args.year2, args.team, args.metric)
