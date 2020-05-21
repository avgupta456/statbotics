from helper import read_tba
from helper import utils

def getTeamInfo(number):
    data = read_tba.get("team/frc"+str(number)+"/simple")
    name, state, country = data["nickname"], data["state_prov"], data["country"]
    region = state if country=="USA" else country

    years = len(read_tba.get("team/frc"+str(number)+"/years_participated"))

    try: district = read_tba.get("team/frc"+str(number)+"/districts")[-1]["abbreviation"]
    except Exception as e: district = "None"

    return [name, region, district, years]

def saveAllTeamsInfo():
    out = {}
    for team in utils.loadAllTeams():
        out[team] = getTeamInfo(team)
        print(out[team])
    utils.saveAllTeamsInfo(out)

if __name__ == "__main__":
    #saveAllTeamsInfo()
    print(utils.loadAllTeamsInfo())
