import unittest
import warnings

from statbotics import main


class TestTeams(unittest.TestCase):
    sb = main.Statbotics()

    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)

    def tearDown(self):
        warnings.simplefilter("default", ResourceWarning)

    def test_get_team(self):
        self.assertEqual(self.sb.get_team(254)["team"], 254)
        self.assertEqual(self.sb.get_team(1323)["team"], 1323)
        self.assertEqual(self.sb.get_team(5511)["team"], 5511)

    def test_get_team_invalid(self):
        with self.assertRaises(UserWarning):
            self.sb.get_team(2)
        with self.assertRaises(TypeError):
            self.sb.get_team("abc")  # type: ignore

    def test_get_team_fields(self):
        a = self.sb.get_team(5511, fields=["team", "country", "state", "district"])
        self.assertEqual(len(a.values()), 4)
        self.assertEqual(a["team"], 5511)
        self.assertEqual(a["country"], "USA")
        self.assertEqual(a["state"], "NC")
        self.assertEqual(a["district"], "fnc")

        b = self.sb.get_team(5511, fields=["team", "norm_epa", "record"])
        self.assertEqual(len(b.values()), 3)
        self.assertEqual(len(b["norm_epa"]), 4)
        self.assertEqual(len(b["record"]), 5)

    def test_get_team_fields_invalid(self):
        with self.assertRaises(ValueError):
            self.sb.get_team(254, fields=["win"])  # should be 'wins'
        with self.assertRaises(ValueError):
            self.sb.get_team(254, fields=["team", "Elo"])

    def test_get_teams(self):
        self.assertTrue(len(self.sb.get_teams()) > 0)

    def test_get_teams_filters(self):
        self.assertTrue(len(self.sb.get_teams(country="usa")) > 0)
        self.assertTrue(len(self.sb.get_teams(country="israel")) > 0)
        self.assertTrue(len(self.sb.get_teams(state="CA")) > 0)
        self.assertTrue(len(self.sb.get_teams(state="california")) > 0)
        self.assertTrue(len(self.sb.get_teams(district="fim")) > 0)

    def test_get_teams_metric(self):
        data = self.sb.get_teams(
            metric="norm_epa", ascending=False, fields=["team", "norm_epa"]
        )
        self.assertTrue(
            data[0]["norm_epa"]["current"] >= data[1]["norm_epa"]["current"]
        )

    def test_get_teams_filters_invalid(self):
        with self.assertRaises(TypeError):
            self.sb.get_teams(country=1)  # type: ignore
        with self.assertRaises(TypeError):
            self.sb.get_teams(state=1)  # type: ignore
        with self.assertRaises(TypeError):
            self.sb.get_teams(district=1)  # type: ignore
        with self.assertRaises(TypeError):
            self.sb.get_teams(limit="a")  # type: ignore
        with self.assertRaises(TypeError):
            self.sb.get_teams(offset="a")  # type: ignore
        with self.assertRaises(TypeError):
            self.sb.get_teams(fields=1)  # type: ignore
        with self.assertRaises(ValueError):
            self.sb.get_teams(metric="test")
        with self.assertRaises(ValueError):
            self.sb.get_teams(country="Canada", state="NC")
