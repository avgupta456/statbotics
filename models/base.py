from abc import ABC, abstractmethod
from typing import Optional


class Model(ABC):
    """Abstract base for match win-probability models.

    The runner calls predict() before a match is played, then update()
    once the result is known.  Models are free to carry state across
    matches and across years.
    """

    @abstractmethod
    def start_year(self, year: int, score_mean: float, score_sd: float, **kwargs) -> None:
        """Called once at the beginning of each season, before any matches."""

    @abstractmethod
    def predict(
        self,
        red1: int,
        red2: int,
        red3: Optional[int],
        blue1: int,
        blue2: int,
        blue3: Optional[int],
    ) -> float:
        """Return P(red wins) in [0, 1], called before the match is played."""

    @abstractmethod
    def update(
        self,
        red1: int,
        red2: int,
        red3: Optional[int],
        blue1: int,
        blue2: int,
        blue3: Optional[int],
        winner: str,        # "red", "blue", or "tie"  (case-insensitive)
        red_score: float,
        blue_score: float,
        elim: bool = False,
    ) -> None:
        """Update internal state after a match result is known."""
