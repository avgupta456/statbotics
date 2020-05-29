import pickle

def dump(path, data):
    with open(path, 'wb') as f:
        pickle.dump(data, f)

def load(file):
    with open(file, 'rb') as f:
        return pickle.load(f)

def saveMatches(year, matches):
    dump("./data/matches/matches_"+str(year)+".p", matches)

def loadMatches(year):
    return load("./data/matches/matches_"+str(year)+".p")

def saveProcessedMatches(year, matches):
    dump("./data/processed_matches/matches_"+str(year)+".p", matches)

def loadProcessedMatches(year):
    return load("./data/processed_matches/matches_"+str(year)+".p")

def saveTeams(year, teams):
    dump("./data/teams/teams_"+str(year)+".p", teams)

def loadTeams(year):
    return load("./data/teams/teams_"+str(year)+".p")

def saveAllTeams(teams):
    dump("./data/teams/teams.p", teams)

def loadAllTeams():
    return load("./data/teams/teams.p")

def saveAllTeamsInfo(teams):
    dump("./data/teams/teams_info.p", teams)

def loadAllTeamsInfo():
    return load("./data/teams/teams_info.p")
