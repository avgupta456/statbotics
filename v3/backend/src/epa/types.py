from typing import Optional, Any

from src.epa.math import SkewNormal


# Rating is represented by a n-dimensional SkewNormal distribution for continuous EPA
# and two Logistic distributions for RP1 and RP2. For some years, RP1 and RP2 are
# replaced by a function of the continuous EPAs. Pre 2016, epa is a 1-dimensional
# SkewNormal and rp_1 and rp_2 are None.


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

    def add_obs(self, epa: Any, alpha: float):
        self.epa.add_obs(epa, alpha)
