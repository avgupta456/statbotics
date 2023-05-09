from typing import Any, List, Tuple

import requests

chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"


def compress(year: int, teams: List[int], match: int) -> str:
    year_binary = bin(year - 2000)[2:]
    match_binary = bin(match)[2:]
    prefix = year_binary.rjust(6, "0") + match_binary.rjust(7, "0")

    teams = sorted(teams)
    teams_binary = [int(bin(team)[2:]) for team in teams]
    lengths = [len(str(team)) for team in teams_binary]
    length_counts = [0 for _ in range(20)]
    for length in lengths:
        length_counts[length] += 1
    pos_lengths_binary = "".join(["1" if x > 0 else "0" for x in length_counts])
    lengths_binary = "".join([bin(x)[2:].rjust(7, "0") for x in length_counts if x > 0])

    binary_string = (
        prefix
        + pos_lengths_binary
        + lengths_binary
        + "".join([str(team) for team in teams_binary])
    )

    binary_string += "0" * (6 - len(binary_string) % 6)

    string = ""
    for i in range(0, len(binary_string), 6):
        string += chars[int(binary_string[i : i + 6], 2)]

    return string


def decompress(string: str) -> Tuple[int, List[int], int]:
    binary_string = ""
    for char in string:
        binary_string += bin(chars.index(char))[2:].rjust(6, "0")

    prefix = binary_string[:13]
    year = int(prefix[:6], 2) + 2000
    match = int(prefix[6:], 2)

    pos_lengths_binary = binary_string[13:33]
    lengths_binary = binary_string[33 : 33 + 7 * pos_lengths_binary.count("1")]
    teams_binary = binary_string[33 + 7 * pos_lengths_binary.count("1") :]

    lengths: List[int] = []
    for i in range(len(pos_lengths_binary)):
        if pos_lengths_binary[i] == "1":
            lengths.append(int(lengths_binary[:7], 2))
            lengths_binary = lengths_binary[7:]
        else:
            lengths.append(0)

    teams: List[int] = []
    for i in range(len(lengths)):
        for _ in range(lengths[i]):
            teams.append(int(teams_binary[:i], 2))
            teams_binary = teams_binary[i:]

    return year, teams, match


def get_cheesy_schedule(num_teams: int, matches_per_team: int) -> List[Any]:
    data = requests.get(
        f"https://raw.githubusercontent.com/Team254/cheesy-arena/main/schedules/{num_teams}_{matches_per_team}.csv"
    )
    lines = data.text.split("\n")
    lines = [[int(x) for x in line.split(",")[::2]] for line in lines[:-1]]
    return lines
