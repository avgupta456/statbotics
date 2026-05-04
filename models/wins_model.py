"""
Wins-rate baseline model.

Each team accumulates a win rate (wins / games played).  A match is predicted
by comparing the average win rate of the red alliance against the blue alliance,
using a simple ratio: P(red) = red_avg / (red_avg + blue_avg).

Teams start with a prior of 1 win and 1 loss (win_rate = 0.5) to avoid
division by zero and to shrink predictions toward 0.5 for teams with little
history — matching the spirit of the blog-post wins baseline.
"""

from typing import Dict, Optional

from base import Model

PRIOR_WINS = 1
PRIOR_GAMES = 2  # implies prior win_rate = 0.5


class WinsModel(Model):
    def __init__(self, carry_across_years: bool = True) -> None:
        """
        Args:
            carry_across_years: If True, win/loss counts persist across seasons.
                                If False, each season resets to the prior.
        """
        self.carry = carry_across_years
        self.wins: Dict[int, float] = {}
        self.games: Dict[int, float] = {}

    def start_year(self, year: int, score_mean: float, score_sd: float, **kwargs) -> None:
        if not self.carry:
            self.wins = {}
            self.games = {}

    def _rate(self, team: int) -> float:
        w = self.wins.get(team, PRIOR_WINS)
        g = self.games.get(team, PRIOR_GAMES)
        return w / g

    def _alliance_avg(self, t1: int, t2: int, t3: Optional[int]) -> float:
        teams = [t for t in (t1, t2, t3) if t is not None]
        return sum(self._rate(t) for t in teams) / len(teams)

    def predict(
        self,
        red1: int, red2: int, red3: Optional[int],
        blue1: int, blue2: int, blue3: Optional[int],
    ) -> float:
        r = self._alliance_avg(red1, red2, red3)
        b = self._alliance_avg(blue1, blue2, blue3)
        return r / (r + b)

    def update(
        self,
        red1: int, red2: int, red3: Optional[int],
        blue1: int, blue2: int, blue3: Optional[int],
        winner: str,
        red_score: float,
        blue_score: float,
        elim: bool = False,
    ) -> None:
        w = winner.upper()
        red_teams = [t for t in (red1, red2, red3) if t is not None]
        blue_teams = [t for t in (blue1, blue2, blue3) if t is not None]

        for t in red_teams:
            self.games[t] = self.games.get(t, PRIOR_GAMES) + 1
            if w == "RED":
                self.wins[t] = self.wins.get(t, PRIOR_WINS) + 1

        for t in blue_teams:
            self.games[t] = self.games.get(t, PRIOR_GAMES) + 1
            if w == "BLUE":
                self.wins[t] = self.wins.get(t, PRIOR_WINS) + 1
