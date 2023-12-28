from typing import Optional, Any

from src.models.epa.math import SkewNormal


class Rating:
    def __init__(
        # self, epa: SkewNormal, rp_1: Optional[Logistic], rp_2: Optional[Logistic]
        self,
        epa: SkewNormal,
        rp_1: Optional[float],
        rp_2: Optional[float],
    ) -> None:
        self.epa = epa
        self.rp_1 = rp_1
        self.rp_2 = rp_2
        self.count = 0

    def add_obs(self, epa: Any, alpha: float, elim: bool):
        self.epa.add_obs(epa, alpha)

        if not elim:
            self.count += 1
