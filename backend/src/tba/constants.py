# DEV SETUP

AUTH_KEY = "XeUIxlvO4CPc44NlLE3ncevDg7bAhp6CRy6zC9M2aQb2zGfys0M30eKwavFJSEJr"


# GEOGRAPHY

USA_MAPPING = {
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

CANADA_MAPPING = {
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

DISTRICT_MAPPING = {
    "mar": "fma",
    "nc": "fnc",
    "tx": "fit",
    "in": "fin",
}


# BLACKLISTS

YEAR_BLACKLIST = [2021]

# 2005va, 2007ga no matches, 2004va quals + elims mismatch
# Rest are incomplete/invalid offseason events
EVENT_BLACKLIST = [
    "2004va",
    "2005va",
    "2007ga",
    "2008cal",  # very incomplete
    "2016cafc2",  # "" team
    "2019lafwbb3",  # too long key, can add back later
    "2022zhha",  # no matches
]

MATCH_BLACKLIST = [
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
]

# 2023 event districts are not autopopulating
# See https://github.com/the-blue-alliance/the-blue-alliance/issues/4936
DISTRICT_OVERRIDES = {
    "2023isde1": "isr",
    "2023isde2": "isr",
    "2023txwac": "fit",
    "2023orore": "pnw",
    "2023nhgrs": "ne",
    "2023mimil": "fim",
    "2023miket": "fim",
    "2023mijac": "fim",
    "2023mifor": "fim",
    "2023miesc": "fim",
    "2023gaalb": "pch",
    "2023wasno": "pnw",
    "2023vabla": "chs",
    "2023txdal": "fit",
    "2023pahat": "fma",
    "2023onnew": "ont",
    "2023onbar": "ont",
    "2023ncash": "fnc",
    "2023mabri": "ne",
    "2023inmis": "fin",
    "2023txbel": "fit",
    "2023orwil": "pnw",
    "2023misjo": "fim",
    "2023milan": "fim",
    "2023mike2": "fim",
    "2023gadal": "pch",
    "2023txcha": "fit",
    "2023scand": "pch",
    "2023rinsc": "ne",
    "2023njfla": "fma",
    "2023ncjoh": "fnc",
    "2023midtr": "fim",
    "2023mdbet": "chs",
    "2023inpri": "fin",
    "2023ctwat": "ne",
    "2023isde3": "isr",
    "2023isde4": "isr",
    "2023wayak": "pnw",
    "2023txsan": "fit",
    "2023txfor": "fit",
    "2023mitvc": "fim",
    "2023mista": "fim",
    "2023mimus": "fim",
    "2023midet": "fim",
    "2023mibel": "fim",
    "2023mawne": "ne",
    "2023wabon": "pnw",
    "2023vapor": "chs",
    "2023vaale": "chs",
    "2023paphi": "fma",
    "2023ontor": "ont",
    "2023onlon": "ont",
    "2023njrob": "fma",
    "2023ncwak": "fnc",
    "2023ncmec": "fnc",
    "2023marea": "ne",
    "2023gagwi": "pch",
    "2023iscmp": "isr",
    "2023txhou": "fit",
    "2023schar": "pch",
    "2023orsal": "pnw",
    "2023onwat": "ont",
    "2023miwmi": "fim",
    "2023mimid": "fim",
    "2023milsu": "fim",
    "2023milak": "fim",
    "2023gacar": "pch",
    "2023wasam": "pnw",
    "2023vagle": "chs",
    "2023onnob": "ont",
    "2023njwas": "fma",
    "2023njtab": "fma",
    "2023nhdur": "ne",
    "2023ncpem": "fnc",
    "2023mitry": "fim",
    "2023mdtim": "chs",
    "2023mabos": "ne",
    "2023inwla": "fin",
    "2023mila2": "fim",
    "2023txama": "fit",
    "2023onwin": "ont",
    "2023mitr2": "fim",
    "2023misal": "fim",
    "2023mimcc": "fim",
    "2023miliv": "fim",
    "2023miken": "fim",
    "2023ingre": "fin",
    "2023gamac": "pch",
    "2023waahs": "pnw",
    "2023txcle": "fit",
    "2023paben": "fma",
    "2023onham": "ont",
    "2023njski": "fma",
    "2023nccmp": "fnc",
    "2023mawor": "ne",
    "2023cthar": "ne",
    "2023txcmp": "fit",
    "2023pncmp": "pnw",
    "2023oncmp": "ont",
    "2023necmp": "ne",
    "2023mrcmp": "fma",
    "2023micmp": "fim",
    "2023incmp": "fin",
    "2023gacmp": "pch",
    "2023chcmp": "chs",
}
