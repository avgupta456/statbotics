import unittest
from typing import Any, cast
from unittest.mock import patch

from fastapi import Response

from src.api.event import read_events
from src.api.match import read_matches
from src.api.team import read_teams
from src.api.team_event import read_team_events
from src.api.team_match import read_team_matches
from src.api.team_year import read_team_years
from src.api.year import read_years


class TestTeamEventSort(unittest.IsolatedAsyncioTestCase):
    async def test_read_endpoints_apply_boolean_ascending_to_metric(self):
        cases = [
            (read_teams, "src.api.team.get_teams_cached", "norm_epa"),
            (read_years, "src.api.year.get_years_cached", "epa_acc"),
            (read_team_years, "src.api.team_year.get_team_years_cached", "epa"),
            (read_events, "src.api.event.get_events_cached", "epa_mean"),
            (read_team_events, "src.api.team_event.get_team_events_cached", "epa"),
            (read_matches, "src.api.match.get_matches_cached", "red_score"),
            (read_team_matches, "src.api.team_match.get_team_matches_cached", "epa"),
        ]

        for read_endpoint, cached_path, metric in cases:
            with self.subTest(endpoint=read_endpoint.__name__):
                with patch(cached_path) as get_cached:
                    get_cached.return_value = []

                    await cast(Any, read_endpoint)(
                        Response(),
                        metric=metric,
                        ascending=True,
                    )

                get_cached.assert_awaited_once()
                await_args = get_cached.await_args
                if await_args is None:
                    self.fail(f"Expected {cached_path} to be awaited")
                self.assertEqual(await_args.kwargs["metric"], metric)
                self.assertTrue(await_args.kwargs["ascending"])


if __name__ == "__main__":
    unittest.main()
