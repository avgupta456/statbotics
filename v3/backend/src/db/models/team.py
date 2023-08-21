from typing import Optional

from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.orm import mapped_column, Mapped

from src.db.main import Base
from src.db.models.main import ModelORM, Model, generate_attr_class


class TeamORM(Base, ModelORM):
    """DECLARATION"""

    __tablename__ = "teams"
    team: Mapped[str] = mapped_column(
        String(6), index=True, nullable=False, primary_key=True
    )

    """GENERAL"""
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    offseason: Mapped[bool] = mapped_column(Boolean, nullable=False)
    country: Mapped[Optional[str]] = mapped_column(String(30))
    district: Mapped[Optional[str]] = mapped_column(String(10))
    state: Mapped[Optional[str]] = mapped_column(String(10))
    rookie_year: Mapped[Optional[int]] = mapped_column(Integer)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False)

    """EPA"""
    norm_epa: Mapped[Optional[float]] = mapped_column(Float)
    norm_epa_recent: Mapped[Optional[float]] = mapped_column(Float)
    norm_epa_mean: Mapped[Optional[float]] = mapped_column(Float)
    norm_epa_max: Mapped[Optional[float]] = mapped_column(Float)

    """STATS"""
    wins: Mapped[int] = mapped_column(Integer, nullable=False)
    losses: Mapped[int] = mapped_column(Integer, nullable=False)
    ties: Mapped[int] = mapped_column(Integer, nullable=False)
    count: Mapped[int] = mapped_column(Integer, nullable=False)
    winrate: Mapped[float] = mapped_column(Float, nullable=False)

    full_wins: Mapped[int] = mapped_column(Integer, nullable=False)
    full_losses: Mapped[int] = mapped_column(Integer, nullable=False)
    full_ties: Mapped[int] = mapped_column(Integer, nullable=False)
    full_count: Mapped[int] = mapped_column(Integer, nullable=False)
    full_winrate: Mapped[float] = mapped_column(Float, nullable=False)


_Team = generate_attr_class("Team", TeamORM)


class Team(_Team, Model):
    def pk(self: "Team") -> str:
        return self.team

    def __str__(self: "Team") -> str:
        # Only refresh DB if these change (during 1 min partial update)
        return f"{self.team}_{self.count}"
