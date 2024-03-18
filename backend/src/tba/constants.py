from typing import Dict, List

# DEV SETUP

AUTH_KEY = "XeUIxlvO4CPc44NlLE3ncevDg7bAhp6CRy6zC9M2aQb2zGfys0M30eKwavFJSEJr"


# GEOGRAPHY

USA_MAPPING: Dict[str, str] = {
    "Alabama": "AL",
    "Alaska": "AK",
    "American Samoa": "AS",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "District of Columbia": "DC",
    "Florida": "FL",
    "Georgia": "GA",
    "Guam": "GU",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Northern Mariana Islands": "MP",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Puerto Rico": "PR",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virgin Islands": "VI",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
}

CANADA_MAPPING: Dict[str, str] = {
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
    "Nunavut": "NU",
}

DISTRICT_MAPPING: Dict[str, str] = {
    "mar": "fma",
    "nc": "fnc",
    "tx": "fit",
    "in": "fin",
}


# TEAMS

PLACEHOLDER_TEAMS = [
    "9999",
    "9998",
    "9997",
    "9996",
    "9995",
    "9994",
    "9993",
    "9992",
    "9991",
    "9990",
    "9989",
    "9988",
    "9987",
    "9986",
    "9985",
    "9984",
    "9983",
    "9982",
    "9981",
    "9980",
]


# BLACKLISTS

# 2005va, 2007ga no matches, 2004va quals + elims mismatch
# Rest are incomplete/invalid offseason events
EVENT_BLACKLIST: List[str] = [
    "2004va",
    "2005va",
    "2007ga",
    "2008cal",  # very incomplete
    "2016cafc2",  # "" team
    "2022zhha",  # no matches
    "2024nywz",  # malformed
]

MATCH_BLACKLIST: List[str] = [
    "2014cafc2_qm4",  # duplicate teams
    "2016mttd_qm13",  # duplicate teams
    "2016mttd_qm18",  # duplicate teams
    "2016mttd_qm30",  # duplicate teams
    "2016ohsc_qf1m1",  # 0's
    "2016ohsc_qf1m2",  # 0's
    "2016ohsc_qf3m1",  # 0's
    "2016ohsc_qf3m2",  # 0's
    "2017crc_qf3m1",  # duplicate teams
    "2019wiwi_ef2m1",  # 58 /
    "2019wiwi_ef5m1",  # 58 /
    "2019wiwi_qf3m1",  # 58 /
    "2024onbar_sf12m1",
    "2024onbar_sf13m1",
    "2024onbar_f1m1",
    "2024onbar_f1m2",
    "2024cala_sf13m1",
    "2024cala_f1m1",
    "2024cala_f1m2",
]

DISTRICT_OVERRIDES: Dict[str, str] = {}
