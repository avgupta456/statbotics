import requests

'''
Helper class to read the TheBlueAlliance (TBA) API
'''

auth_key = "XeUIxlvO4CPc44NlLE3ncevDg7bAhp6CRy6zC9M2aQb2zGfys0M30eKwavFJSEJr"
read_pre = "https://www.thebluealliance.com/api/v3/"

session = requests.Session()
session.headers.update({'X-TBA-Auth-Key': auth_key, 'X-TBA-Auth-Id': ''})


def get(url): return session.get(read_pre+url).json()
