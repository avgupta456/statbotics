from collections import defaultdict
from typing import Any, Dict, List

from src.models.epa_v2_math import t_prob_gt_0, SkewNormal
from src.models.epa_v2_breakdown import (
    all_keys,
    all_headers,
    expand_breakdown,
    post_process_breakdown,
    get_score_from_breakdown,
    get_pred_rps,
)
from src.classes import Attribution, Match, Pred, YearStats
from src.models.template import Model

import numpy as np


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
            year, self.stats.breakdown_mean, self.stats.breakdown_mean, True
        )
        sd = (overall_sd / overall_mean) * mean

        if year == 2018:
            # normalize scale rating to 0 mean
            mean[-5] = 0

        self.counts: Dict[int, int] = defaultdict(int)
        self.epas: Dict[int, SkewNormal] = defaultdict(
            lambda: SkewNormal(mean / 3, np.square(sd / 3), 0)
        )

        self.defense_epas: Dict[int, SkewNormal] = defaultdict(
            lambda: SkewNormal(np.array([0]), np.array([1]), 0)
        )

        self.fouls_epas: Dict[int, SkewNormal] = defaultdict(
            lambda: SkewNormal(np.array([0]), np.array([1]), 0)
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
            # opp_pred_sd = np.array([np.sqrt(self.epas[t].var) for t in opp_teams]).sum(axis=0)  # type: ignore

            pred_mean = post_process_breakdown(
                self.stats.year, match.key, pred_mean, opp_pred_mean
            )

            pred_defense = np.array([self.defense_epas[t].mean for t in teams]).sum(axis=0)  # type: ignore
            pred_fouls = np.array([self.fouls_epas[t].mean for t in teams]).sum(axis=0)  # type: ignore

            pred_rp_1, pred_rp_2 = get_pred_rps(
                self.stats.year, match.week, pred_mean, pred_sd
            )

            rp_1s.append(pred_rp_1)
            rp_2s.append(pred_rp_2)

            breakdowns.append(
                {"offense": pred_mean, "defense": pred_defense, "fouls": pred_fouls}
            )

        year = self.stats.year
        playoff = match.playoff

        foul_rate = (
            self.stats.breakdown_mean["foul_points"]
            / self.stats.breakdown_mean["no_foul_points"]
        )

        red_score = get_score_from_breakdown(
            year,
            breakdowns[0]["offense"],
            breakdowns[1]["offense"],
            rp_1s[0],
            rp_2s[0],
            playoff,
        )

        blue_score = get_score_from_breakdown(
            year,
            breakdowns[1]["offense"],
            breakdowns[0]["offense"],
            rp_1s[1],
            rp_2s[1],
            playoff,
        )

        score_diff = red_score - blue_score
        # teams are fully correlated by construction
        red_sd = sum([self.epas[t].var[0] ** 0.5 for t in match.red()])
        blue_sd = sum([self.epas[t].var[0] ** 0.5 for t in match.blue()])
        # assume alliances are -0.5 correlated
        corr = 0.5
        total_sd = (red_sd**2 + blue_sd**2 + 2 * corr * red_sd * blue_sd) ** 0.5
        win_prob = t_prob_gt_0(score_diff, total_sd)

        # K = 5 / 8
        # norm_diff = (blue_score - red_score) / self.stats.score_sd
        # win_prob = 1 / (1 + 10 ** (K * norm_diff))

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
        for teams, bd, opp_bd, pred_bd, opp_pred_bd in [
            (match.red(), red_bd, blue_bd, pred.red_breakdown, pred.blue_breakdown),
            (match.blue(), blue_bd, red_bd, pred.blue_breakdown, pred.red_breakdown),
        ]:
            offense_error = bd - pred_bd["offense"]
            defense_error = (opp_pred_bd["offense"] - opp_bd).sum() - pred_bd["defense"]
            fouls_error = np.array([opp_bd[1]]) - pred_bd["fouls"]

            for t in teams:
                offense_attrib = self.epas[t].mean + offense_error / 3
                defense_attrib = self.defense_epas[t].mean + defense_error / 3
                fouls_attrib = self.fouls_epas[t].mean + fouls_error / 3

                # Don't update RP score during playoff match
                # Do update in 2016 since incentivized
                year = self.stats.year
                if year == 2018 and match.playoff:
                    rp_1_index = all_keys[year].index("rp_1_power")
                    offense_attrib[rp_1_index] = self.epas[t].mean[rp_1_index]

                    rp_2_index = all_keys[year].index("rp_2_power")
                    offense_attrib[rp_2_index] = self.epas[t].mean[rp_2_index]

                out[t] = Attribution(
                    offense_attrib[0],
                    {
                        "offense": offense_attrib,
                        "defense": defense_attrib,
                        "fouls": fouls_attrib,
                    },
                )

        return out

    def update_team(self, team: int, attr: Attribution, match: Match) -> None:
        weight = 1 / 3 if match.playoff else 1
        percent = self.percent_func(self.counts[team])
        alpha = percent * weight

        self.epas[team].add_obs(attr.breakdown["offense"], alpha)
        self.defense_epas[team].add_obs(
            attr.breakdown["defense"], alpha / 2, only_pos=True
        )
        self.fouls_epas[team].add_obs(attr.breakdown["fouls"], alpha / 2, only_pos=True)

        if not match.playoff:
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

            if year == 2018:
                keys = all_keys[year]
                new_total_points = (
                    x.mean[keys.index("auto_run_points")]
                    + 2 * x.mean[keys.index("auto_switch_secs")]
                    + 4 * x.mean[keys.index("auto_scale_secs")]
                    + 145 * x.mean[keys.index("switch_power")]
                    + 290 * x.mean[keys.index("scale_power")]
                    + 145 * x.mean[keys.index("opp_switch_power")]
                    + x.mean[keys.index("vault_points")]
                    + x.mean[keys.index("endgame_points")]
                )

                new_ratings[t][-2] = new_total_points

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
