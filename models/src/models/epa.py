from typing import Dict
from collections import defaultdict

from src.models.template import Model
from src.classes import Match, Pred, Attribution, YearStats


class EPA(Model):
    @staticmethod
    def percent_func(x: int) -> float:
        return min(0.5, max(0.3, 0.5 - 0.2 / 6 * (x - 6)))

    @staticmethod
    def margin_func(year: int, x: int) -> float:
        if year == 2015:
            return 0

        if year == 2018:
            return 1

        return min(1, max(0, 1 / 24 * (x - 12)))

    def start_season(self, stats: YearStats) -> None:
        super().start_season(stats)

        year, mean, sd = self.stats.year, self.stats.score_mean, self.stats.score_sd

        self.counts: Dict[int, int] = defaultdict(int)
        self.epa: Dict[int, float] = defaultdict(lambda: mean / 3 - 0.2 * sd)
        for team in set(self.end_ratings[year - 1]).union(self.end_ratings[year - 2]):
            year_1 = self.end_ratings[year - 1].get(team, 1500)
            year_2 = self.end_ratings[year - 2].get(team, 1500)
            old_epa = 0.7 * year_1 + 0.3 * year_2
            new_epa = 0.6 * old_epa + 0.4 * 1500
            self.epa[team] = mean / 3 + sd * (new_epa - 1500) / 250

    def predict_match(self, match: Match) -> Pred:
        red_epa = sum(self.epa[t] for t in match.red())
        blue_epa = sum(self.epa[t] for t in match.blue())

        K = 5 / 8
        norm_diff = (blue_epa - red_epa) / self.stats.score_sd
        win_prob = 1 / (1 + 10 ** (K * norm_diff))

        return Pred(red_epa, blue_epa, win_prob)

    def attribute_match(self, match: Match, pred: Pred) -> Dict[int, Attribution]:
        out: Dict[int, Attribution] = {}

        red_error = match.red_no_fouls - pred.red_score
        blue_error = match.blue_no_fouls - pred.blue_score

        for t in match.red():
            margin = self.margin_func(self.stats.year, self.counts[t])
            error = (red_error - margin * blue_error) / (1 + margin)
            out[t] = Attribution(self.epa[t] + error / 3)

        for t in match.blue():
            margin = self.margin_func(self.stats.year, self.counts[t])
            error = (blue_error - margin * red_error) / (1 + margin)
            out[t] = Attribution(self.epa[t] + error / 3)

        return out

    def update_team(self, team: int, attr: Attribution, playoff: bool) -> None:
        update = attr.contrib - self.epa[team]

        percent = self.percent_func(self.counts[team])
        weight = 1 / 3 if playoff else 1

        self.epa[team] += percent * weight * update
        self.counts[team] += 0 if playoff else 1

    def end_season(self) -> None:
        super().end_season()

        year, mean, sd = self.stats.year, self.stats.score_mean, self.stats.score_sd
        for team in self.epa:
            epa = 1500 + 250 * (self.epa[team] - mean / 3) / sd
            self.end_ratings[year][team] = epa
