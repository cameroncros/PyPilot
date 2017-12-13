import unittest
from unittest import mock

from pypilot.planner.coordinate import Coordinate
from pypilot.planner.geoutils import calc_tracking, calc_magnetic_offset, calc_tracking_magnetic
from pypilot.planner.waypoint import WayPoint

WAN = (-37.4083, 144.9767)
BPN = (-37.9833, 144.3500)


class GeoUtilTest(unittest.TestCase):

    def test_calc_tracking(self):
        self.assertEqual(0, calc_tracking(WayPoint(coordinate=Coordinate(0, 0)),
                                          WayPoint(coordinate=Coordinate(90, 0))))
        self.assertEqual(180, calc_tracking(WayPoint(coordinate=Coordinate(0, 0)),
                                            WayPoint(coordinate=Coordinate(-90, 0))))
        self.assertEqual(90, calc_tracking(WayPoint(coordinate=Coordinate(0, 0)),
                                           WayPoint(coordinate=Coordinate(0, 90))))
        self.assertEqual(270, calc_tracking(WayPoint(coordinate=Coordinate(0, 0)),
                                            WayPoint(coordinate=Coordinate(0, -90))))
        self.assertAlmostEqual(220.6, calc_tracking(WayPoint(coordinate=WAN), WayPoint(coordinate=BPN)), 1)

    # Location of Magnetic North (2017) - http://wdc.kugi.kyoto-u.ac.jp/poles/polesexp.html
    # noinspection PyUnusedLocal
    @mock.patch('pypilot.planner.config.Config.get_magnetic_north',
                return_value=(80.4, 72.8))
    def test_calc_magnetic_offset(self, get_magnetic_north_function):
        self.assertAlmostEqual(-11.1, calc_magnetic_offset(
            WayPoint(coordinate=Coordinate(-37.8136, 144.9631))), 1)  # Melbourne CBD, should be +12

    # Location of Magnetic North (2017) - http://wdc.kugi.kyoto-u.ac.jp/poles/polesexp.html
    # noinspection PyUnusedLocal
    @mock.patch('pypilot.planner.config.Config.get_magnetic_north',
                return_value=(80.4, 72.8))
    def test_calc_tracking_magnetic(self, get_magnetic_north_function):
        self.assertAlmostEqual(209.5, calc_tracking_magnetic(WayPoint(coordinate=WAN), WayPoint(coordinate=BPN)), 1)
