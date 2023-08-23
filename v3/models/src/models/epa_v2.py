from collections import defaultdict
from typing import Any, Dict, List

import numpy as np

from src.classes import Attribution, Match, Pred, YearStats
from src.models.epa_v2_breakdown import (
    all_headers,
    expand_breakdown,
    get_pred_rps,
    get_score_from_breakdown,
    post_process_attrib,
    post_process_breakdown,
)
from src.models.epa_v2_math import SkewNormal
from src.models.template import Model


class EPAV2(Model):
    @staticmethod
    def percent_func(x: int) -> float:
        return min(0.5, max(0.3, 0.5 - 0.2 / 6 * (x - 6)))

    def start_season(self, stats: YearStats) -> None:
        super().start_season(stats)

        year = self.stats.year
        overall_mean = self.stats.score_mean
        overall_sd = self.stats.score_sd

        mean = expand_breakdown(
            year, self.stats.breakdown_mean, self.stats.breakdown_mean
        )
        sd = (overall_sd / overall_mean) * mean

        if year == 2018:
            # normalize scale rating to 0 mean
            mean[-5] = 0

        self.counts: Dict[int, int] = defaultdict(int)
        self.epas: Dict[int, SkewNormal] = defaultdict(
            lambda: SkewNormal(mean / 3 - 0.2 * sd, np.square(sd / 3), 0)
        )

        for t in set(self.end_ratings[year - 1]).union(self.end_ratings[year - 2]):
            year_1 = self.end_ratings[year - 1].get(t, 0)
            year_2 = self.end_ratings[year - 2].get(t, 0)
            old_epa = 0.7 * year_1 + 0.3 * year_2
            new_epa = 0.6 * old_epa  # mean reversion
            self.epas[t] = SkewNormal(mean / 3 + new_epa * sd, sd / 3, 0)

    def predict_match(self, match: Match) -> Pred:
        rp_1s: List[float] = []
        rp_2s: List[float] = []
        breakdowns: List[Any] = []

        for teams, opp_teams in [
            (match.red(), match.blue()),
            (match.blue(), match.red()),
        ]:
            pred_mean = np.array([self.epas[t].mean for t in teams]).sum(axis=0)  # type: ignore
            pred_sd = np.array([np.sqrt(self.epas[t].var) for t in teams]).sum(axis=0)  # type: ignore
            opp_pred_mean = np.array([self.epas[t].mean for t in opp_teams]).sum(axis=0)  # type: ignore

            pred_mean = post_process_breakdown(
                self.stats.year, match.key, pred_mean, opp_pred_mean
            )

            pred_rp_1, pred_rp_2 = get_pred_rps(
                self.stats.year, match.week, pred_mean, pred_sd
            )

            rp_1s.append(pred_rp_1)
            rp_2s.append(pred_rp_2)
            breakdowns.append(pred_mean)

        year = self.stats.year
        elim = match.elim

        red_score = get_score_from_breakdown(
            year, breakdowns[0], breakdowns[1], rp_1s[0], rp_2s[0], elim
        )

        blue_score = get_score_from_breakdown(
            year, breakdowns[1], breakdowns[0], rp_1s[1], rp_2s[1], elim
        )

        # Could also use variance to get win probability
        # But this is simpler, less noisy, and more tested

        K = 5 / 8
        norm_diff = (blue_score - red_score) / self.stats.score_sd
        win_prob = 1 / (1 + 10 ** (K * norm_diff))

        foul_rate = (
            self.stats.breakdown_mean["foul_points"]
            / self.stats.breakdown_mean["no_foul_points"]
        )

        return Pred(
            red_score * (1 + foul_rate),
            blue_score * (1 + foul_rate),
            win_prob,
            rp_1s[0],
            rp_1s[1],
            rp_2s[0],
            rp_2s[1],
            breakdowns[0],
            breakdowns[1],
        )

    def attribute_match(self, match: Match, pred: Pred) -> Dict[int, Attribution]:
        out: Dict[int, Attribution] = {}

        year = self.stats.year
        red_bd = expand_breakdown(year, match.red_breakdown, match.blue_breakdown)
        blue_bd = expand_breakdown(year, match.blue_breakdown, match.red_breakdown)
        for teams, bd, pred_bd in [
            (match.red(), red_bd, pred.red_breakdown),
            (match.blue(), blue_bd, pred.blue_breakdown),
        ]:
            for t in teams:
                attrib = self.epas[t].mean + (bd - pred_bd) / 3
                attrib = post_process_attrib(
                    year, self.epas[t].mean, attrib, match.elim
                )
                out[t] = Attribution(attrib[0], attrib)

        return out

    def update_team(self, team: int, attrib: Attribution, match: Match) -> None:
        weight = 1 / 3 if match.elim else 1
        percent = self.percent_func(self.counts[team])
        alpha = percent * weight

        self.epas[team].add_obs(attrib.breakdown, alpha)

        if not match.elim:
            self.counts[team] += 1

    def end_season(self) -> None:
        super().end_season()

        year, mean, sd = self.stats.year, self.stats.score_mean, self.stats.score_sd
        for team in self.epas:
            self.end_ratings[year][team] = (self.epas[team].mean[0] - mean / 3) / sd

        self.print_ratings()

    def print_ratings(self) -> None:
        year = self.stats.year

        N = 10

        new_ratings: Dict[int, Any] = {}
        for t in self.epas:
            x = self.epas[t]

            lower, upper = x.mean_conf_interval()

            new_ratings[t] = x.mean[2:].tolist() + [lower[0], x.mean[0], upper[0]]

        overall_ratings = sorted(
            new_ratings.items(), key=lambda x: x[1][-2], reverse=True
        )

        print(f"Overall ratings for {year}:")
        print(all_headers[year])
        for team, x in overall_ratings[:N]:
            print(
                str(team) + "\t" + "\t".join([str(round(c, 2)) for c in x]),
            )
        print()
