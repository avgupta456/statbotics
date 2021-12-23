from requests import Session

auth_key = "XeUIxlvO4CPc44NlLE3ncevDg7bAhp6CRy6zC9M2aQb2zGfys0M30eKwavFJSEJr"
read_prefix = "https://www.thebluealliance.com/api/v3/"

session = Session()
session.headers.update({"X-TBA-Auth-Key": auth_key, "X-TBA-Auth-Id": ""})


def get_tba(url: str):
    return session.get(read_prefix + url).json()


# 2005va, 2007ga no matches, 2004va quals + elims mismatch, 2020wasp only elims
event_blacklist = ["2004va", "2005va", "2007ga", "2020waspo"]
