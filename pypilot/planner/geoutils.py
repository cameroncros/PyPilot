import math

from geopy.distance import great_circle

from pypilot.planner.config import Config
from pypilot.planner.coordinate import Coordinate
from pypilot.planner.waypoint import WayPoint


def calc_tracking(current_waypoint, next_waypoint):
    """
        https://gist.github.com/jeromer/2005586
        Calculates the bearing between two points.
        The formulae used is the following:
            θ = atan2(sin(Δlong).cos(lat2),
                      cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
        :Parameters:
          - `current: The current waypoint
          - `next: The next waypoint
        :Returns:
          The bearing in degrees
        :Returns Type:
          float
        """
    point_a = tuple(current_waypoint.coordinate)
    point_b = tuple(next_waypoint.coordinate)

    lat1 = math.radians(point_a[0])
    lat2 = math.radians(point_b[0])

    diff_long = math.radians(point_b[1] - point_a[1])

    x = math.sin(diff_long) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
                                           * math.cos(lat2) * math.cos(diff_long))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing


def calc_magnetic_offset(current_waypoint):
    offset = calc_tracking(current_waypoint, WayPoint(coordinate=Config().get_magnetic_north()))
    if offset > 180:
        offset -= 360
    return offset


def calc_tracking_magnetic(current_waypoint, next_waypoint):
    true_bearing = calc_tracking(current_waypoint, next_waypoint)

    return true_bearing + calc_magnetic_offset(current_waypoint)

def calc_distance(current_waypoint, next_waypoint):
    return great_circle(tuple(current_waypoint.coordinate), tuple(next_waypoint.coordinate)).nautical
