from enum import Enum


class MatchWinner(str, Enum):
    RED = "red"
    BLUE = "blue"
    TIE = "tie"


class MatchStatus(str, Enum):
    UPCOMING = "Upcoming"
    COMPLETED = "Completed"


class CompLevel(str, Enum):
    INVALID = "invalid"
    QUAL = "qm"
    EIGHTH = "ef"
    QUARTER = "qf"
    SEMI = "sf"
    FINAL = "f"


class EventStatus(str, Enum):
    INVALID = "Invalid"
    UPCOMING = "Upcoming"
    ONGOING = "Ongoing"
    COMPLETED = "Completed"


class EventType(str, Enum):
    INVALID = "invalid"
    REGIONAL = "regional"
    DISTRICT = "district"
    DISTRICT_CMP = "district_cmp"
    CHAMPS_DIV = "champs_div"
    EINSTEIN = "einstein"
    # OFFSEASON = "offseason"

    def is_champs(self: "EventType") -> bool:
        return self in (EventType.CHAMPS_DIV, EventType.EINSTEIN)
