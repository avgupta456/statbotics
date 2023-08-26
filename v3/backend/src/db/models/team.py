from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.orm import mapped_column

from src.db.main import Base
from src.db.models.main import Model, ModelORM, generate_attr_class
from src.db.models.types import MB, MF, MI, MOF, MOI, MOS, MS


class TeamORM(Base, ModelORM):
    """DECLARATION"""

    __tablename__ = "teams"
    team: MS = mapped_column(String(6), index=True, primary_key=True)

    """NO DEFAULTS"""
    name: MS = mapped_column(String(100))
    country: MOS = mapped_column(String(30), nullable=True)
    state: MOS = mapped_column(String(10), nullable=True)
    rookie_year: MOI = mapped_column(Integer, nullable=True)

    """GENERAL"""
    offseason: MB = mapped_column(Boolean, default=True)
    district: MOS = mapped_column(String(10), nullable=True, default=None)
    active: MB = mapped_column(Boolean, default=False)

    """STATS"""
    wins: MI = mapped_column(Integer, default=0)
    losses: MI = mapped_column(Integer, default=0)
    ties: MI = mapped_column(Integer, default=0)
    count: MI = mapped_column(Integer, default=0)
    winrate: MF = mapped_column(Float, default=0)

    full_wins: MI = mapped_column(Integer, default=0)
    full_losses: MI = mapped_column(Integer, default=0)
    full_ties: MI = mapped_column(Integer, default=0)
    full_count: MI = mapped_column(Integer, default=0)
    full_winrate: MF = mapped_column(Float, default=0)

    """EPA"""
    norm_epa: MOF = mapped_column(Float, nullable=True, default=None)
    norm_epa_recent: MOF = mapped_column(Float, nullable=True, default=None)
    norm_epa_mean: MOF = mapped_column(Float, nullable=True, default=None)
    norm_epa_max: MOF = mapped_column(Float, nullable=True, default=None)


_Team = generate_attr_class("Team", TeamORM)


class Team(_Team, Model):
    def pk(self: "Team") -> str:
        return self.team

    def __hash__(self: "Team") -> int:
        return hash(self.pk())

    def __str__(self: "Team") -> str:
        # Only refresh DB if these change (during 1 min partial update)
        return f"{self.team}_{self.count}"
