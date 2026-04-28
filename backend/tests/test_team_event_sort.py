import unittest
from typing import Any, cast
from unittest.mock import patch

from fastapi import Response

from src.api.event import read_events
from src.api.match import read_matches
from src.api.query import resolve_sort_direction
from src.api.team import read_teams
from src.api.team_event import read_team_events
from src.api.team_match import read_team_matches
from src.api.team_year import read_team_years
from src.api.year import read_years


class TestTeamEventSort(unittest.IsolatedAsyncioTestCase):
    def test_resolve_sort_direction_uses_sort_when_present(self):
        self.assertTrue(resolve_sort_direction(None, "asc"))
        self.assertTrue(resolve_sort_direction(False, "ascending"))
        self.assertFalse(resolve_sort_direction(None, "desc"))
        self.assertFalse(resolve_sort_direction(True, "descending"))

    def test_resolve_sort_direction_preserves_ascending_without_sort(self):
        self.assertTrue(resolve_sort_direction(True, None))
        self.assertFalse(resolve_sort_direction(False, None))
        self.assertIsNone(resolve_sort_direction(None, None))

    def test_resolve_sort_direction_rejects_invalid_sort(self):
        with self.assertRaises(ValueError):
            resolve_sort_direction(None, cast(Any, "epa"))

    async def test_read_endpoints_apply_sort_direction_to_metric(self):
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
                        sort="asc",
                    )

                get_cached.assert_awaited_once()
                await_args = get_cached.await_args
                if await_args is None:
                    self.fail(f"Expected {cached_path} to be awaited")
                self.assertEqual(await_args.kwargs["metric"], metric)
                self.assertTrue(await_args.kwargs["ascending"])


if __name__ == "__main__":
    unittest.main()
