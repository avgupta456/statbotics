import pickle

def dump(path, data):
    with open(path, 'wb') as f:
        pickle.dump(data, f)

def load(file):
    with open(file, 'rb') as f:
        return pickle.load(f)

def saveMatches(year, matches):
    dump("./matches/matches_"+str(year)+".p", matches)

def loadMatches(year):
    return load("./matches/matches_"+str(year)+".p")

def saveProcessedMatches(year, matches):
    dump("./processed_matches/matches_"+str(year)+".p", matches)

def loadProcessedMatches(year):
    return load("./processed_matches/matches_"+str(year)+".p")

def saveTeams(year, teams):
    dump("./teams/teams_"+str(year)+".p", teams)

def loadTeams(year):
    return load("./teams/teams_"+str(year)+".p")
