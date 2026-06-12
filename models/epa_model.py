"""
Simplified EPA model (total-score only).

Faithfully reproduces the core statbotics EPA logic without the
breakdown-component machinery:

  - Cross-year initialization via normalized EPA with mean reversion.
  - Per-match EWMA update: epa += weight * percent * (error / num_teams)
  - Win probability: 1 / (1 + 10^(k * norm_diff))

This is equivalent to the full EPA model run on pre-2016 data (where only
the total score is tracked), and a faithful approximation for later years.
"""

from typing import Dict, Optional

from base import Model

# ── Constants (mirrors src/models/epa/constants.py) ──────────────────────────
NORM_MEAN = 1500.0
NORM_SD = 250.0
INIT_PENALTY = 0.2          # new/unknown teams start slightly below average
MEAN_REVERSION = 0.4        # fraction pulled back toward baseline each season
YEAR_ONE_WEIGHT = 0.7       # weight of most-recent prior year vs year-2
ELIM_WEIGHT = 1 / 3         # elim matches count 1/3 as much as quals

INIT_NORM_EPA = NORM_MEAN - INIT_PENALTY * NORM_SD  # 1450


# ── Helpers ───────────────────────────────────────────────────────────────────

def _k(year: int) -> float:
    """Logistic k-factor for win probability."""
    return -5 / 8 if year >= 2008 else -5 / 12


def _percent(year: int, count: int) -> float:
    """EWMA learning rate.  Mirrors EPA.percent_func in the backend."""
    prev = min(0.5, max(0.3, 0.5 - 0.2 / 6 * (count - 6)))
    return 2 / 3 * prev if year >= 2016 else 0.5 * prev


def _to_norm(epa: float, score_mean: float, score_sd: float, num_teams: int) -> float:
    return NORM_MEAN + NORM_SD * (epa - score_mean / num_teams) / score_sd


def _from_norm(
    norm_epa: float, score_mean: float, score_sd: float, num_teams: int
) -> float:
    return max(0.0, score_mean / num_teams + score_sd * (norm_epa - NORM_MEAN) / NORM_SD)


# ── Model ─────────────────────────────────────────────────────────────────────

class EPAModel(Model):
    """EPA model that operates on total match score."""

    def __init__(self) -> None:
        # Normalized EPAs persist across years (keyed by team number).
        # We store two snapshots to mirror the backend's year-1 / year-2 blend.
        self._norm_epa_1: Dict[int, float] = {}  # most recent year-end EPA
        self._norm_epa_2: Dict[int, float] = {}  # year before that

        # Current-season state (reset each year)
        self.epas: Dict[int, float] = {}
        self.counts: Dict[int, int] = {}
        self.year = 0
        self.score_mean = 1.0
        self.score_sd = 1.0
        self.num_teams = 3
        self.k = _k(2008)

    # ── Lifecycle ────────────────────────────────────────────────────────────

    def start_year(
        self, year: int, score_mean: float, score_sd: float, **kwargs
    ) -> None:
        if self.year > 0:
            self._snapshot_year()

        self.year = year
        self.score_mean = score_mean
        self.score_sd = max(score_sd, 1.0)  # guard against zero
        self.num_teams = 2 if year <= 2004 else 3
        self.k = _k(year)
        self.counts = {}

        # Roll prior normalized EPAs forward with mean reversion.
        new_epas: Dict[int, float] = {}
        all_teams = set(self._norm_epa_1) | set(self._norm_epa_2)
        for t in all_teams:
            n1 = self._norm_epa_1.get(t, INIT_NORM_EPA)
            n2 = self._norm_epa_2.get(t, INIT_NORM_EPA)
            prev_norm = YEAR_ONE_WEIGHT * n1 + (1 - YEAR_ONE_WEIGHT) * n2
            curr_norm = (1 - MEAN_REVERSION) * prev_norm + MEAN_REVERSION * INIT_NORM_EPA
            new_epas[t] = _from_norm(curr_norm, score_mean, self.score_sd, self.num_teams)
        self.epas = new_epas

    def _snapshot_year(self) -> None:
        """Rotate current EPAs into the cross-year history."""
        self._norm_epa_2 = dict(self._norm_epa_1)
        for team, epa in self.epas.items():
            self._norm_epa_1[team] = _to_norm(
                epa, self.score_mean, self.score_sd, self.num_teams
            )

    def _epa(self, team: int) -> float:
        """Return current EPA, initializing from prior history if first seen."""
        if team not in self.epas:
            n1 = self._norm_epa_1.get(team, INIT_NORM_EPA)
            n2 = self._norm_epa_2.get(team, INIT_NORM_EPA)
            prev_norm = YEAR_ONE_WEIGHT * n1 + (1 - YEAR_ONE_WEIGHT) * n2
            curr_norm = (1 - MEAN_REVERSION) * prev_norm + MEAN_REVERSION * INIT_NORM_EPA
            self.epas[team] = _from_norm(
                curr_norm, self.score_mean, self.score_sd, self.num_teams
            )
        return self.epas[team]

    # ── Prediction ───────────────────────────────────────────────────────────

    def predict(
        self,
        red1: int, red2: int, red3: Optional[int],
        blue1: int, blue2: int, blue3: Optional[int],
    ) -> float:
        red = [t for t in (red1, red2, red3) if t is not None]
        blue = [t for t in (blue1, blue2, blue3) if t is not None]

        red_sum = sum(self._epa(t) for t in red)
        blue_sum = sum(self._epa(t) for t in blue)
        norm_diff = (red_sum - blue_sum) / self.score_sd
        return 1.0 / (1.0 + 10.0 ** (self.k * norm_diff))

    # ── Update ───────────────────────────────────────────────────────────────

    def update(
        self,
        red1: int, red2: int, red3: Optional[int],
        blue1: int, blue2: int, blue3: Optional[int],
        winner: str,
        red_score: float,
        blue_score: float,
        elim: bool = False,
    ) -> None:
        red = [t for t in (red1, red2, red3) if t is not None]
        blue = [t for t in (blue1, blue2, blue3) if t is not None]
        n = len(red)  # same for both alliances
        weight = ELIM_WEIGHT if elim else 1.0

        for teams, actual in ((red, red_score), (blue, blue_score)):
            pred = sum(self._epa(t) for t in teams)
            error = actual - pred
            for t in teams:
                pct = _percent(self.year, self.counts.get(t, 0))
                self.epas[t] = self._epa(t) + weight * pct * error / n

        if not elim:
            for t in red + blue:
                self.counts[t] = self.counts.get(t, 0) + 1
