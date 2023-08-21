from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.orm import mapped_column

from src.db.main import Base
from src.db.models.main import ModelORM, Model, generate_attr_class
from src.db.models.types import MS, MB, MOS, MOI, MI, MF, MOF


class TeamORM(Base, ModelORM):
    """DECLARATION"""

    __tablename__ = "teams"
    team: MS = mapped_column(String(6), index=True, primary_key=True)

    """GENERAL"""
    name: MS = mapped_column(String(100))
    offseason: MB = mapped_column(Boolean)
    country: MOS = mapped_column(String(30))
    district: MOS = mapped_column(String(10))
    state: MOS = mapped_column(String(10))
    rookie_year: MOI = mapped_column(Integer)
    active: MB = mapped_column(Boolean)

    """EPA"""
    norm_epa: MOF = mapped_column(Float)
    norm_epa_recent: MOF = mapped_column(Float)
    norm_epa_mean: MOF = mapped_column(Float)
    norm_epa_max: MOF = mapped_column(Float)

    """STATS"""
    wins: MI = mapped_column(Integer)
    losses: MI = mapped_column(Integer)
    ties: MI = mapped_column(Integer)
    count: MI = mapped_column(Integer)
    winrate: MF = mapped_column(Float)

    full_wins: MI = mapped_column(Integer)
    full_losses: MI = mapped_column(Integer)
    full_ties: MI = mapped_column(Integer)
    full_count: MI = mapped_column(Integer)
    full_winrate: MF = mapped_column(Float)


_Team = generate_attr_class("Team", TeamORM)


class Team(_Team, Model):
    def pk(self: "Team") -> str:
        return self.team

    def __str__(self: "Team") -> str:
        # Only refresh DB if these change (during 1 min partial update)
        return f"{self.team}_{self.count}"
