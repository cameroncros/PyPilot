import os
import unittest

from pypilot.planner.planner import Planner


class PlannerTest(unittest.TestCase):
    planner = None

    def setUp(self):
        self.planner = Planner()
        self.planner.load_waypoint_list("test_positions.csv")

        waypoint = self.planner.read_waypoint("(12.345, 67.89)")
        self.assertIsNotNone(waypoint)
        self.planner.waypoints.append(waypoint)

        waypoint = self.planner.read_waypoint("KNO")
        self.assertIsNotNone(waypoint)
        self.planner.waypoints.append(waypoint)

    def tearDown(self):
        pass

    def test_save_waypoints(self):
        self.planner.save_waypoints("test.csv")

        expected = "PSN,TRK (T),TRK (M-est),DIST\n" \
                   "\"(12.3450, 67.8900)\"\n" \
                   "KNO,120.27362151018747,120.27362151018747,4415.289745753938\n"

        self.assertTrue(os.path.isfile("test.csv"))

        with open("test.csv", "r") as file:
            actual = file.read()
            self.assertEqual(expected, actual)

        os.remove("test.csv")

    def test_load_waypoints(self):
        self.planner.save_waypoints("test.csv")

        planner2 = Planner()
        planner2.load_waypoints("test.csv")
        self.assertEqual(2, len(planner2.waypoints))

        # Should not add duplicates
        planner2.load_waypoints("test.csv")
        self.assertEqual(2, len(planner2.waypoints))

        self.assertEqual("(12.3450, 67.8900)", planner2.waypoints[0].get_waypoint())
        self.assertEqual("KNO", planner2.waypoints[1].get_waypoint())

        os.remove("test.csv")
