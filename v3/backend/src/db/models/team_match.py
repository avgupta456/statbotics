from typing import Any, Dict, Optional

import attr
from sqlalchemy import Boolean, Column, Float, Integer, String  # type: ignore
from sqlalchemy.sql.schema import (  # type: ignore
    ForeignKeyConstraint,
    PrimaryKeyConstraint,
)

from src.db.main import Base
from src.db.models.main import ModelORM, generate_attr_class


class TeamMatchORM(Base, ModelORM):
    """DECLARATION"""

    __tablename__ = "team_matches"
    id: int = Column(Integer)  # placeholder for backend API
    team: str = Column(String(6), index=True)
    year: int = Column(Integer, index=True)
    event: str = Column(String(20), index=True)
    match: str = Column(String(20), index=True)
    alliance: str = Column(String(6), index=True)

    PrimaryKeyConstraint(team, match)
    ForeignKeyConstraint(["year"], ["years.year"])
    ForeignKeyConstraint(["team"], ["teams.team"])
    ForeignKeyConstraint(["event"], ["events.key"])
    ForeignKeyConstraint(["match"], ["matches.key"])
    ForeignKeyConstraint(["team", "year"], ["team_years.team", "team_years.year"])
    ForeignKeyConstraint(["team", "event"], ["team_events.team", "team_events.event"])
    ForeignKeyConstraint(
        ["match", "alliance"], ["alliances.match", "alliances.alliance"]
    )

    """GENERAL"""
    time: int = Column(Integer)
    offseason: bool = Column(Boolean)
    playoff: bool = Column(Boolean)
    alliance: str = Column(String(6))

    dq: bool = Column(Boolean)
    surrogate: bool = Column(Boolean)

    # Choices are 'Upcoming', 'Completed'
    status: str = Column(String(10))

    epa: float = Column(Float)
    auto_epa: float = Column(Float)
    teleop_epa: float = Column(Float)
    endgame_epa: float = Column(Float)
    rp_1_epa: float = Column(Float)
    rp_2_epa: float = Column(Float)

    post_epa: Optional[float] = Column(Float)


_TeamMatch = generate_attr_class("TeamMatch", TeamMatchORM)


class TeamMatch(_TeamMatch):
    @classmethod
    def from_dict(cls, dict: Dict[str, Any]) -> "TeamMatch":
        dict = {k: dict.get(k, None) for k in cls.__slots__}  # type: ignore
        return TeamMatch(**dict)

    def as_dict(self: "TeamMatch") -> Dict[str, Any]:
        return attr.asdict(
            self,  # type: ignore
            filter=attr.filters.exclude(attr.fields(TeamMatch).id),  # type: ignore
        )

    """
    HELPER FUNCTIONS
    """

    def to_dict(self: "TeamMatch") -> Dict[str, Any]:
        return {k: getattr(self, k) for k in self.__slots__}  # type: ignore

    """PARENT FUNCTIONS"""

    def sort(self: "TeamMatch") -> int:
        return self.time

    def pk(self: "TeamMatch") -> str:
        return f"{self.team}_{self.match}"

    def __str__(self: "TeamMatch") -> str:
        # Only refresh DB if these change (during 1 min partial update)
        return f"{self.team}_{self.match}_{self.status}_{self.epa}_{self.post_epa}"
