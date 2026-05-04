from typing import Any, Dict, Optional

import attr


@attr.s(auto_attribs=True, slots=True, hash=False, eq=False)
class TeamMatch:
    """In-memory only — not persisted to DB. EPA data is stored on TeamYear and Match."""

    id: Optional[int] = None
    team: int = 0
    year: int = 0
    event: str = ""
    match: str = ""
    alliance: str = ""
    time: int = 0
    week: int = 0
    elim: bool = False
    dq: bool = False
    surrogate: bool = False
    status: str = "Upcoming"

    epa: float = 0
    auto_epa: Optional[float] = None
    teleop_epa: Optional[float] = None
    endgame_epa: Optional[float] = None
    rp_1_epa: Optional[float] = None
    rp_2_epa: Optional[float] = None
    rp_3_epa: Optional[float] = None
    tiebreaker_epa: Optional[float] = None
    comp_1_epa: Optional[float] = None
    comp_2_epa: Optional[float] = None
    comp_3_epa: Optional[float] = None
    comp_4_epa: Optional[float] = None
    comp_5_epa: Optional[float] = None
    comp_6_epa: Optional[float] = None
    comp_7_epa: Optional[float] = None
    comp_8_epa: Optional[float] = None
    comp_9_epa: Optional[float] = None
    comp_10_epa: Optional[float] = None
    comp_11_epa: Optional[float] = None
    comp_12_epa: Optional[float] = None
    comp_13_epa: Optional[float] = None
    comp_14_epa: Optional[float] = None
    comp_15_epa: Optional[float] = None
    comp_16_epa: Optional[float] = None
    comp_17_epa: Optional[float] = None
    comp_18_epa: Optional[float] = None
    post_epa: Optional[float] = None

    def sort(self) -> int:
        return self.time

    def pk(self) -> str:
        return f"{self.team}_{self.match}"

    def __hash__(self) -> int:
        return hash(self.pk())

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, TeamMatch):
            return False
        return self.pk() == other.pk()

    def __str__(self) -> str:
        return "_".join(
            [str(self.team), self.match, str(self.status), str(self.epa), str(self.post_epa)]
        )

    def to_compact_dict(self) -> Dict[str, Any]:
        """Compact representation stored on TeamYear.team_matches."""
        return {
            "match": self.match,
            "event": self.event,
            "alliance": self.alliance,
            "time": self.time,
            "week": self.week,
            "elim": self.elim,
            "status": self.status,
            "epa": self.epa,
            "auto_epa": self.auto_epa,
            "teleop_epa": self.teleop_epa,
            "endgame_epa": self.endgame_epa,
            "rp_1_epa": self.rp_1_epa,
            "rp_2_epa": self.rp_2_epa,
            "rp_3_epa": self.rp_3_epa,
            "post_epa": self.post_epa,
        }

    def to_epa_dict(self) -> Dict[str, Any]:
        """EPA-only representation stored in Match.team_epas[team]."""
        return {
            "epa": self.epa,
            "auto_epa": self.auto_epa,
            "teleop_epa": self.teleop_epa,
            "endgame_epa": self.endgame_epa,
            "rp_1_epa": self.rp_1_epa,
            "rp_2_epa": self.rp_2_epa,
            "rp_3_epa": self.rp_3_epa,
            "post_epa": self.post_epa,
        }
