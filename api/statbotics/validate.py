from typing import Any, List, Optional, Tuple, Union

from .constants import countries, districts, USA, Canada


def check_type(val: Optional[Union[int, str, List[Any]]], type: str, name: str) -> None:
    if not val:
        return None
    if type == "int" and not isinstance(val, int):
        raise TypeError("'" + name + "' must be an integer")
    if type == "str" and not isinstance(val, str):
        raise TypeError("'" + name + "' must be a string")
    if type == "list" and not isinstance(val, list):
        raise TypeError("'" + name + "' must be a list")


def get_country(country: str) -> str:
    if country.lower() in countries:
        return "%20".join(countries[country.lower()].split(" "))
    raise ValueError("Not a valid country")


def get_state(country: Optional[str], state: str) -> Tuple[str, str]:
    if country not in [None, "USA", "Canada"]:
        raise ValueError("Can only specify state for USA, Canada")

    if state.lower() in USA:
        return "USA", USA[state.lower()]
    if state.upper() in USA.values():
        return "USA", state

    if state.lower() in Canada:
        return "Canada", Canada[state.lower()]
    if state.upper() in Canada.values():
        return "Canada", state

    raise ValueError("Not a valid state")


def get_district(district: str) -> str:
    if district.lower() in districts:
        return districts[district.lower()]
    raise ValueError("Not a valid district")


def get_locations(
    country: Optional[str], state: Optional[str], district: Optional[str]
) -> str:
    check_type(country, "str", "country")
    check_type(state, "str", "state")
    check_type(district, "str", "district")

    if country and district:
        raise ValueError("Cannot specify country and district")
    if state and district:
        raise ValueError("Cannot specify state and district")

    url = ""

    if country:
        country = get_country(country)
        url += "&country=" + country

    if state:
        temp_country, state = get_state(country, state)
        if country and temp_country != country:
            raise ValueError("State from different country")
        if not country:
            url += "&country=" + temp_country
        url += "&state=" + state

    if district:
        district = get_district(district)
        url += "&district=" + district

    return url


def get_type(type: Optional[Union[int, str]]) -> Optional[int]:
    if type is None:
        return None
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

    raise ValueError(
        "Enter a valid type (0 - regional, 1 - district, 2 - district champs, 3 - worlds, 4 - einstein)"
    )
