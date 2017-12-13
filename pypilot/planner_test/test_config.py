import os
import unittest

from pypilot.planner.config import Config


class ConfigTest(unittest.TestCase):
    config = Config()

    @classmethod
    def setUpClass(cls):
        with open("config.json", "w") as file:
            file.write("{\n"
                       "  \"magnetic_north\": [80.31, 72.62],\n"  # Correct as of 2015
                       "  \"waypoint_files\": [\"waypoints.csv\"]\n"
                       "}\n")

    @classmethod
    def tearDownClass(cls):
        os.remove("config.json")

    def test_load_config(self):
        self.config.config = None
        self.config.load_config()
        self.assertIsNotNone(self.config.config)

    def test_get_magnetic_north(self):
        self.config.load_config()
        magnetic_north = self.config.get_magnetic_north()
        self.assertEqual((80.31, 72.62), magnetic_north)

    def test_get_waypoint_lists(self):
        self.config.load_config()
        waypoint_lists = self.config.get_waypoint_lists()
        self.assertEqual(["waypoints.csv"], waypoint_lists)
