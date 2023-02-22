import unittest
import warnings

from statbotics import main


class TestFramework(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)

    def tearDown(self):
        warnings.simplefilter("default", ResourceWarning)

    def test_create_statbotics(self):
        sb = main.Statbotics()
        return sb
