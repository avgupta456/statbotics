import requests
from helper import utils

USA = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands': 'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}

Canada = {
    "Newfoundland": "NL",
    "Prince Edward Island": "PE",
    "Nova Scotia": "NS",
    "New Brunswick": "NB",
    "Québec": "QC",
    "Ontario": "ON",
    "Manitoba": "MB",
    "Saskatchewan": "SK",
    "Alberta": "AB",
    "British Columbia": "BC",
    "Yukon": "YT",
    "Northwest Territories": "NT",
    "Nunavut": "NU"
}

districts = {
    "mar": "fma",
    "nc": "fnc",
    "tx": "fit",
    "in": "fin",
}


auth_key = "XeUIxlvO4CPc44NlLE3ncevDg7bAhp6CRy6zC9M2aQb2zGfys0M30eKwavFJSEJr"
read_pre = "https://www.thebluealliance.com/api/v3/"
session = requests.Session()
session.headers.update({'X-TBA-Auth-Key': auth_key, 'X-TBA-Auth-Id': ''})


def get(url):
    return session.get(read_pre+url).json()


def getTeamInfo(number):
    data = get("team/frc"+str(number)+"/simple")
    name = data["nickname"]
    state = data["state_prov"]
    country = data["country"]

    years = len(get("team/frc"+str(number)+"/years_participated"))

    try:
        district = get("team/frc"+str(number)+"/districts")[-1]["abbreviation"]
    except Exception:
        district = "None"

    if(state in USA):
        state = USA[state]
    elif(state in Canada):
        state = Canada[state]
    elif(country != "USA" and country != "Canada"):
        state = "All"

    if(district in districts):
        district = districts[district]

    return [name, country, state, district, years]


def saveAllTeamsInfo():
    out = utils.loadAllTeamsInfo()
    count = 0

    for team in utils.loadAllTeams():
        count += 1

        if count % 100 == 0:
            print(count)
            utils.saveAllTeamsInfo(out)

        if team in out:
            pass
        else:
            out[team] = getTeamInfo(team)

    utils.saveAllTeamsInfo(out)


def cleanState(state):
    if state in USA:
        return USA[state]
    if state in Canada:
        return Canada[state]
    return "All"


def cleanDistrict(district):
    if district in districts:
        return districts[district]
    return district


def getMatchTime(match, event_time):
    if match["actual_time"] is not None:
        return match["actual_time"]

    match_time = event_time  # start value
    if match["comp_level"] == "qm":
        match_time += match["match_number"]
    elif match["comp_level"] == "qf":
        match_time += 200 + 10 * match["set_number"] + match["match_number"]
    elif match["comp_level"] == "sf":
        match_time += 400 + 10 * match["set_number"] + match["match_number"]
    else:
        match_time += 600 + match["match_number"]
    return match_time


def getBreakdown(breakdown=None, year=2020):
    if breakdown is None or year < 2016:
        out = {
            "auto": -1, "auto_movement": -1, "auto_1": -1, "auto_2": -1,
            "auto_2_1": -1, "auto_2_2": -1, "auto_2_3": -1, "teleop_1": -1,
            "teleop_2": -1, "teleop_2_1": -1, "teleop_2_2": -1,
            "teleop_2_3": -1, "1": -1, "2": -1, "teleop": -1,
            "endgame": -1, "no_fouls": -1, "fouls": -1, "rp1": -1,
            "rp2": -1
        }
        return out
    if year == 2016:
        out = {
            "auto": breakdown["autoPoints"],
            "auto_movement": breakdown["autoReachPoints"],
            "auto_1": breakdown["autoCrossingPoints"],
            "auto_2": breakdown["autoBoulderPoints"],
            "auto_2_1": breakdown["autoBouldersLow"] * 5,
            "auto_2_2": breakdown["autoBouldersHigh"] * 10,
            "auto_2_3": 0,
            "teleop_1": breakdown["teleopCrossingPoints"],
            "teleop_2": breakdown["teleopBoulderPoints"],
            "teleop_2_1": breakdown["teleopBouldersLow"] * 2,
            "teleop_2_2": breakdown["teleopBouldersHigh"] * 5,
            "teleop_2_3": 0,
        }
        out["1"] = out["auto_1"] + out["teleop_1"]
        out["2"] = out["auto_2"] + out["teleop_2"]
        out["teleop"] = out["teleop_1"] + out["teleop_2"]
        out["endgame"] = breakdown["teleopChallengePoints"]
        out["no_fouls"] = out["auto"] + out["teleop"] + out["endgame"]
        out["fouls"] = breakdown["foulPoints"]
        out["rp1"] = breakdown["teleopDefensesBreached"]
        out["rp2"] = breakdown["teleopTowerCaptured"]
        return out
    if year == 2017:
        out = {
            "auto": breakdown["autoPoints"],
            "auto_movement": breakdown["autoMobilityPoints"],
            "auto_1": breakdown["autoRotorPoints"],
            "auto_2": breakdown["autoFuelPoints"],
            "auto_2_1": breakdown["autoFuelLow"],
            "auto_2_2": breakdown["autoFuelHigh"],
            "auto_2_3": 0,
            "teleop_1": breakdown["teleopRotorPoints"],
            "teleop_2": breakdown["teleopFuelPoints"],
            "teleop_2_1": breakdown["teleopFuelLow"],
            "teleop_2_2": breakdown["teleopFuelHigh"],
            "teleop_2_3": 0,
        }
        out["1"] = out["auto_1"] + out["teleop_1"]
        out["2"] = out["auto_2"] + out["teleop_2"]
        out["teleop"] = out["teleop_1"] + out["teleop_2"]
        out["endgame"] = breakdown["teleopTakeoffPoints"]
        out["no_fouls"] = out["auto"] + out["teleop"] + out["endgame"]
        out["fouls"] = breakdown["foulPoints"]
        out["rp1"] = 1 if breakdown["rotorRankingPointAchieved"] else 0
        out["rp2"] = 1 if breakdown["kPaRankingPointAchieved"] else 0
        return out
    if year == 2018:
        out = {
            "auto": breakdown["autoPoints"],
            "auto_movement": breakdown["autoRunPoints"],
            "auto_1": 0,
            "auto_2": breakdown["autoOwnershipPoints"],
            "auto_2_1": breakdown["autoSwitchOwnershipSec"] * 2,
            "auto_2_2": breakdown["autoScaleOwnershipSec"] * 2,
            "auto_2_3": 0,
            "teleop_1": breakdown["vaultPoints"],
            "teleop_2": breakdown["teleopOwnershipPoints"],
            "teleop_2_1": breakdown["teleopSwitchOwnershipSec"],
            "teleop_2_2": breakdown["teleopScaleOwnershipSec"],
            "teleop_2_3": 0,
        }
        out["1"] = out["auto_1"] + out["teleop_1"]
        out["2"] = out["auto_2"] + out["teleop_2"]
        out["teleop"] = out["teleop_1"] + out["teleop_2"]
        out["endgame"] = breakdown["endgamePoints"]
        out["no_fouls"] = out["auto"] + out["teleop"] + out["endgame"]
        out["fouls"] = breakdown["foulPoints"]
        out["rp1"] = 1 if breakdown["autoQuestRankingPoint"] else 0
        out["rp2"] = 1 if breakdown["faceTheBossRankingPoint"] else 0
        return out
    if year == 2019:
        out = {
            "auto": breakdown["autoPoints"],
            "auto_movement": breakdown["sandStormBonusPoints"],
            "auto_1": 0,
            "auto_2": 0,
            "auto_2_1": 0,
            "auto_2_2": 0,
            "auto_2_3": 0,
            "teleop_1": breakdown["hatchPanelPoints"],
            "teleop_2": breakdown["cargoPoints"],
            "teleop_2_1": 0,
            "teleop_2_2": 0,
            "teleop_2_3": 0,
        }
        out["1"] = out["auto_1"] + out["teleop_1"]
        out["2"] = out["auto_2"] + out["teleop_2"]
        out["teleop"] = out["teleop_1"] + out["teleop_2"]
        out["endgame"] = breakdown["habClimbPoints"]
        out["no_fouls"] = out["auto"] + out["teleop"] + out["endgame"]
        out["fouls"] = breakdown["foulPoints"]
        out["rp1"] = 1 if breakdown["completeRocketRankingPoint"] else 0
        out["rp2"] = 1 if breakdown["habDockingRankingPoint"] else 0
        return out
    if year == 2020:
        out = {
            "auto": breakdown["autoPoints"],
            "auto_movement": breakdown["autoInitLinePoints"],
            "auto_1": 0,
            "auto_2": breakdown["autoCellPoints"],
            "auto_2_1": breakdown["autoCellsBottom"] * 2,
            "auto_2_2": breakdown["autoCellsOuter"] * 4,
            "auto_2_3": breakdown["autoCellsInner"] * 6,
            "teleop_1": breakdown["controlPanelPoints"],
            "teleop_2": breakdown["teleopCellPoints"],
            "teleop_2_1": breakdown["teleopCellsBottom"],
            "teleop_2_2": breakdown["teleopCellsOuter"] * 2,
            "teleop_2_3": breakdown["teleopCellsInner"] * 3,
        }
        out["1"] = out["auto_1"] + out["teleop_1"]
        out["2"] = out["auto_2"] + out["teleop_2"]
        out["teleop"] = out["teleop_1"] + out["teleop_2"]
        out["endgame"] = breakdown["endgamePoints"]
        out["no_fouls"] = out["auto"] + out["teleop"] + out["endgame"]
        out["fouls"] = breakdown["foulPoints"]
        out["rp1"] = 1 if breakdown["shieldEnergizedRankingPoint"] else 0
        out["rp2"] = 1 if breakdown["shieldOperationalRankingPoint"] else 0
        return out
