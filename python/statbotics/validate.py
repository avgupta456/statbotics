countries = {
    "united states of america": "USA",
    "united states": "USA",
    "america": "USA",
    "usa": "USA",
    "canada": "Canada",
    "turkey": "Turkey",
    "israel": "Israel",
    "china": "China",
    "mexico": "Mexico",
    "australia": "Australia",
    "brazil": "Brazil",
    "chinese taipei": "Chinese Taipei",
    "netherlands": "Netherlands",
    "chile": "Chile",
    "united kingdom": "United Kingdom",
    "uk": "United Kingdom",
    "colombia": "Colombia",
    "japan": "Japan",
    "poland": "Poland",
    "india": "India",
    "switzerland": "Switzerland"
}

USA = {
    "alabama": "AL",
    "alaska": "AK",
    "american samoa": "AS",
    "arizona": "AZ",
    "arkansas": "AR",
    "california": "CA",
    "colorado": "CO",
    "connecticut": "CT",
    "delaware": "DE",
    "district of columbia": "DC",
    "florida": "FL",
    "georgia": "GA",
    "guam": "GU",
    "hawaii": "HI",
    "idaho": "ID",
    "illinois": "IL",
    "indiana": "IN",
    "iowa": "IA",
    "kansas": "KS",
    "kentucky": "KY",
    "louisiana": "LA",
    "maine": "ME",
    "maryland": "MD",
    "massachusetts": "MA",
    "michigan": "MI",
    "minnesota": "MN",
    "mississippi": "MS",
    "missouri": "MO",
    "montana": "MT",
    "nebraska": "NE",
    "nevada": "NV",
    "new hampshire": "NH",
    "new jersey": "NJ",
    "new mexico": "NM",
    "new york": "NY",
    "north carolina": "NC",
    "north dakota": "ND",
    "northern mariana islands": "MP",
    "ohio": "OH",
    "oklahoma": "OK",
    "oregon": "OR",
    "pennsylvania": "PA",
    "puerto Rico": "PR",
    "rhode island": "RI",
    "south carolina": "SC",
    "south dakota": "SD",
    "tennessee": "TN",
    "texas": "TX",
    "utah": "UT",
    "vermont": "VT",
    "virgin islands": "VI",
    "virginia": "VA",
    "washington": "WA",
    "west virginia": "WV",
    "wisconsin": "WI",
    "wyoming": "WY"
}

Canada = {
    "newfoundland": "NL",
    "prince edward island": "PE",
    "nova scotia": "NS",
    "new brunswick": "NB",
    "québec": "QC",
    "quebec": "QC",
    "ontario": "ON",
    "manitoba": "MB",
    "saskatchewan": "SK",
    "alberta": "AB",
    "british columbia": "BC",
    "yukon": "YT",
    "northwest territories": "NT",
    "nunavut": "NU"
}

districts = {
    "mar": "fma",
    "fma": "fma",
    "nc": "fnc",
    "fnc": "fnc",
    "tx": "fit",
    "fit": "fit",
    "in": "fin",
    "fin": "fin",

    "fim": "fim",
    "ne": "ne",
    "chs": "chs",
    "ont": "ont",
    "pnw": "pnw",
    "pch": "pch",
    "isr": "isr"
}

team_metrics = ["elo", "-elo", "elo_recent", "-elo_recent", "elo_mean",
                "-elo_mean", "elo_max", "-elo_max"]


def getCountry(country):
    if country.lower() in countries:
        return "%20".join(countries[country.lower()].split(" "))
    raise ValueError("Not a valid country")


def getState(country, state):
    if country not in [None, "USA", "Canada"]:
        raise ValueError("Can only specify state for USA, Canada")

    if state.lower() in USA:
        return "USA", USA[state.lower()]
    if state.upper() in USA.values():
        return "USA", state

    if state.lower() in Canada:
        return "Canda", Canada[state.lower()]
    if state.upper() in Canada.values():
        return "Canada", state

    raise ValueError("Not a valid state")


def getDistrict(district):
    if district.lower() in districts:
        return districts[district.lower()]
    raise ValueError("Not a valid district")


def getTeamMetrics():
    return team_metrics
