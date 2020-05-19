import utils
import argparse
import elo

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--action', type=str, help='action', default='lookup', required=True)
    parser.add_argument('-t', '--team', type=int, help="team", required=False)
    parser.add_argument('-y', '--year', type=str, help="year", required=True)
    return parser.parse_args()

def lookup(year, team, metric):
    teams = utils.loadTeams(year)
    team = teams[team]

    ratings = team.ratings
    rating = team.get_rating_max()

    for i in range(len(ratings)):
        print(str(i+1)+":\t"+str(ratings[i]))
    print("Max:   " + str(rating))

def leaderboard(year, rating):
    teams = utils.loadTeams(year)
    board = sorted(teams.values())[:25]
    for i in range(len(board)):
        print(str(i+1)+"\t"+str(board[i].number)+"\t"+str(board[i].get_rating_max()))

def rank(year, team, print=True):
    teams = utils.loadTeams(year)
    num_teams = len(teams)

    ratings = []
    for t in teams.values(): elos.append(t.get_rating_max())
    ratings.sort()

    rank = num_teams-ratings.index(teams[team].get_rating_max())
    percent = int(1000*rank/num_teams)/10

    if(print): print("Rank:\t" + str(rank) + "\t(Top " + str(percent) + "%)")
    return rank

def ranks(start_year, team):
    for year in range(int(start_year), 2020):
        print(str(year)+"\t"+str(rank(year, team, False))+"/"+str(len(utils.loadTeams(year))))

if __name__ == "__main__":
    args = get_args()
    if(args.action=="lookup"): lookup(args.year, args.team)
    elif(args.action=="leaderboard"): leaderboard(args.year)
    elif(args.action=="rank"): rank(args.year, args.team)
    elif(args.action=="ranks"): ranks(args.year, args.team)
