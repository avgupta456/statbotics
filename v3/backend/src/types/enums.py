from enum import Enum


class AllianceColor(str, Enum):
    RED = "red"
    BLUE = "blue"


class MatchWinner(str, Enum):
    RED = "red"
    BLUE = "blue"
    TIE = "tie"


class MatchStatus(str, Enum):
    UPCOMING = "Upcoming"
    COMPLETED = "Completed"


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
    OFFSEASON = "offseason"
    PRESEASON = "preseason"

    def is_offseason(self: "EventType") -> bool:
        return self in (EventType.OFFSEASON, EventType.PRESEASON)

    def is_champs(self: "EventType") -> bool:
        return self in (EventType.CHAMPS_DIV, EventType.EINSTEIN)


class CompLevel(str, Enum):
    INVALID = "invalid"
    QUAL = "qm"
    EIGHTH = "ef"
    QUARTER = "qf"
    SEMI = "sf"
    FINAL = "f"
