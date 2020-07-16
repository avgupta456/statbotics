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

team_year_metrics = ["elo_start", "-elo_start", "elo_pre_champs",
                     "-elo_pre_champs", "elo_end", "-elo_end", "elo_mean",
                     "-elo_mean", "elo_max", "-elo_max", "elo_diff",
                     "-elo_diff", "opr", "-opr", "opr_auto", "-opr_auto",
                     "opr_1", "-opr_1", "opr_2", "-opr_2", "opr_endgame",
                     "-opr_endgame", "opr_fouls", "-opr_fouls", "opr_no_fouls",
                     "-opr_no_fouls", "ils_1", "-ils_1", "ils_2", "-ils_2"]

event_metrics = ['elo_top8', '-elo_top8', 'elo_top24', '-elo_top24',
                 'elo_mean', '-elo_mean', 'opr_top8', '-opr_top8',
                 'opr_top24', '-opr_top24', 'opr_mean', '-opr_mean']

team_event_metrics = ['elo_start', '-elo_start', 'elo_pre_playoffs',
                      '-elo_pre_playoffs', 'elo_end', '-elo_end', 'elo_mean',
                      '-elo_mean', 'elo_max', '-elo_max', 'elo_diff',
                      '-elo_diff', 'opr_start', '-opr_start', 'opr_end',
                      '-opr_end', 'ils_1', '-ils_1', 'ils_2', '-ils_2']


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


def getLocations(country, state, district):
    checkType(country, "str", "country")
    checkType(state, "str", "state")
    checkType(district, "str", "district")

    if country and district:
        raise ValueError("Cannot specify country and district")
    if state and district:
        raise ValueError("Cannot specify state and district")

    url = ""

    if country:
        country = getCountry(country)
        url += "/country/" + country

    if state:
        temp_country, state = getState(country, state)
        if country and temp_country != country:
            raise ValueError("State from different country")
        if not country:
            url += "/country/" + temp_country
        url += "/state/" + state

    if district:
        district = getDistrict(district)
        url += "/district/" + district

    return url


def getType(type):
    if not type:
        return
    if isinstance(type, int):
        return type
    if "regional" in type.lower():
        return 0
    if type.lower() == "district":
        return 1
    if "district champ" in type.lower():
        return 2
    if "world" in type.lower():
        return 3
    if "einstein" in type.lower():
        return 4

    raise ValueError("Enter a valid type (0 - regional, 1 - district, " +
                     + "2 - district champs, 3 - worlds, 4 - einstein)")


def checkType(val, type, name):
    if not val:
        return
    if type == "int" and not isinstance(val, int):
        raise TypeError("'"+name+"' must be an integer")
    if type == "str" and not isinstance(val, str):
        raise TypeError("'"+name+"' must be a string")


def getTeamMetrics():
    return team_metrics


def getTeamYearMetrics():
    return team_year_metrics


def getEventMetrics():
    return event_metrics


def getTeamEventMetrics():
    return team_event_metrics
