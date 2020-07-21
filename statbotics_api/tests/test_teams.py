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
        self.assertEqual(self.sb.getTeam(148)["team"], 148)
        self.assertEqual(self.sb.getTeam(254)["team"], 254)
        self.assertEqual(self.sb.getTeam(5511)["team"], 5511)

    def test_get_team_invalid(self):
        with self.assertRaises(UserWarning):
            self.sb.getTeam(2)
        with self.assertRaises(TypeError):
            self.sb.getTeam("abc")

    def test_get_team_fields(self):
        a = self.sb.getTeam(5511, fields=["team", "country", "state", "district"])
        self.assertEqual(len(a.values()), 4)
        self.assertEqual(a["team"], 5511)
        self.assertEqual(a["country"], "USA")
        self.assertEqual(a["state"], "NC")
        self.assertEqual(a["district"], "fnc")

        b = self.sb.getTeam(
            5511, fields=["team", "elo", "elo_recent", "elo_mean", "elo_max"]
        )
        self.assertEqual(len(b.values()), 5)

    def test_get_team_fields_invalid(self):
        with self.assertRaises(ValueError):
            self.sb.getTeam(254, fields=["wins"])
        with self.assertRaises(ValueError):
            self.sb.getTeam(254, fields=["team", "ELO"])

    def test_get_teams(self):
        self.assertTrue(len(self.sb.getTeams()) > 0)

    def test_get_teams_filters(self):
        self.assertTrue(len(self.sb.getTeams(country="usa")) > 0)
        self.assertTrue(len(self.sb.getTeams(country="israel")) > 0)
        self.assertTrue(len(self.sb.getTeams(state="CA")) > 0)
        self.assertTrue(len(self.sb.getTeams(state="california")) > 0)
        self.assertTrue(len(self.sb.getTeams(district="fim")) > 0)

    def test_get_teams_metric(self):
        data = self.sb.getTeams(country="USA", metric="elo", fields=["team", "elo"])
        self.assertTrue(data[0]["elo"] >= data[1]["elo"])

        data = self.sb.getTeams(metric="-elo_recent")
        self.assertTrue(data[0]["elo_recent"] <= data[1]["elo_recent"])

    def test_get_teams_filters_invalid(self):
        with self.assertRaises(TypeError):
            self.sb.getTeams(country=1)
        with self.assertRaises(TypeError):
            self.sb.getTeams(state=1)
        with self.assertRaises(TypeError):
            self.sb.getTeams(district=1)
        with self.assertRaises(TypeError):
            self.sb.getTeams(limit="a")
        with self.assertRaises(TypeError):
            self.sb.getTeams(offset="a")
        with self.assertRaises(TypeError):
            self.sb.getTeams(fields=1)
        with self.assertRaises(ValueError):
            self.sb.getTeams(metric="test")
        with self.assertRaises(ValueError):
            self.sb.getTeams(country="Canada", state="NC")
