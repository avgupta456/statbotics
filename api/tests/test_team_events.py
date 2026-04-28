import unittest
import warnings

from statbotics import main


class TestTeamEvents(unittest.TestCase):
    sb = main.Statbotics()

    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)

    def tearDown(self):
        warnings.simplefilter("default", ResourceWarning)

    def test_get_team_events_metric(self):
        data = self.sb.get_team_events(
            event="2026isrtp",
            metric="epa",
            ascending=False,
            fields=["team", "epa"],
        )

        self.assertTrue(
            data[0]["epa"]["total_points"]["mean"]
            >= data[1]["epa"]["total_points"]["mean"]
        )

    def test_get_team_events_legacy_metric_alias(self):
        data = self.sb.get_team_events(
            event="2026isrtp",
            metric="epa_end",
            ascending=False,
            fields=["team", "epa"],
        )

        self.assertTrue(
            data[0]["epa"]["total_points"]["mean"]
            >= data[1]["epa"]["total_points"]["mean"]
        )

    def test_get_team_events_metric_invalid(self):
        with self.assertRaises(ValueError):
            self.sb.get_team_events(event="2026isrtp", metric="epa_diff")


if __name__ == "__main__":
    unittest.main()
