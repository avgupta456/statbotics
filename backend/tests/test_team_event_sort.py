import unittest
from typing import Any, cast
from unittest.mock import patch

from fastapi import Response

from src.api.team_event import _resolve_sort_direction, read_team_events


class TestTeamEventSort(unittest.IsolatedAsyncioTestCase):
    def test_resolve_sort_direction_uses_sort_when_present(self):
        self.assertTrue(_resolve_sort_direction(None, "asc"))
        self.assertTrue(_resolve_sort_direction(False, "ascending"))
        self.assertFalse(_resolve_sort_direction(None, "desc"))
        self.assertFalse(_resolve_sort_direction(True, "descending"))

    def test_resolve_sort_direction_preserves_ascending_without_sort(self):
        self.assertTrue(_resolve_sort_direction(True, None))
        self.assertFalse(_resolve_sort_direction(False, None))
        self.assertIsNone(_resolve_sort_direction(None, None))

    def test_resolve_sort_direction_rejects_invalid_sort(self):
        with self.assertRaises(ValueError):
            _resolve_sort_direction(None, cast(Any, "epa"))

    async def test_read_team_events_applies_sort_direction_to_metric(self):
        with patch("src.api.team_event.get_team_events_cached") as get_team_events:
            get_team_events.return_value = []

            await cast(Any, read_team_events)(
                Response(),
                event="2026isrtp",
                metric="epa",
                sort="asc",
            )

        get_team_events.assert_awaited_once()
        await_args = get_team_events.await_args
        if await_args is None:
            self.fail("Expected get_team_events_cached to be awaited")
        self.assertEqual(await_args.kwargs["metric"], "epa")
        self.assertTrue(await_args.kwargs["ascending"])


if __name__ == "__main__":
    unittest.main()
