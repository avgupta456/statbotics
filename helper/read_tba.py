import requests
'''
Helper class to read the TheBlueAlliance (TBA) API
'''

auth_key = "XeUIxlvO4CPc44NlLE3ncevDg7bAhp6CRy6zC9M2aQb2zGfys0M30eKwavFJSEJr"
read_pre = "https://www.thebluealliance.com/api/v3/"

session = requests.Session()
session.headers.update({'X-TBA-Auth-Key': auth_key, 'X-TBA-Auth-Id': ''})

def get(url): return session.get(read_pre+url).json()


def getTeamInfo(number):
    data = get("team/frc"+str(number)+"/simple")
    name, state, country = data["nickname"], data["state_prov"], data["country"]
    region = state if country=="USA" else country

    years = len(get("team/frc"+str(number)+"/years_participated"))

    try: district = get("team/frc"+str(number)+"/districts")[-1]["abbreviation"]
    except Exception as e: district = "None"

    return [name, region, district, years]

print(getTeamInfo(254))
print(getTeamInfo(5511))
print(getTeamInfo(1690))
