from pypilot.planner.coordinate import Coordinate
from pypilot.planner.latlong import LatLong
from pypilot.planner.waypoint import WayPoint


class WayPointList:
    waypoints = {}

    def __init__(self):
        # Reads the positions.csv file, and parses the entries in the format:
        # ADELAIDE RIVER BRIDGE NT ADB S 12 39.5 E 131 20.0
        with open("positions.csv", 'r') as file:
            for line in file:
                parts = line.split(" ")
                if len(parts) > 8:
                    lat = LatLong.from_parts(direction=parts[-6], degrees=parts[-5], minutes=parts[-4])
                    lon = LatLong.from_parts(direction=parts[-3], degrees=parts[-2], minutes=parts[-1])

                    code = parts[-7]
                    waypoint = WayPoint(code=code, state=parts[-8], location=" ".join(parts[0:-8]),
                                        coordinate=Coordinate(latitude=lat, longitude=lon))

                    if self.waypoints.get(code):
                        print("Duplicate Code found, ignored")
                        continue
                    self.waypoints[code] = waypoint

    def get_waypoint(self, code):
        return self.waypoints.get(code)

    def __str__(self):
        string = ""
        for code in self.waypoints:
            string += "%s\n" % self.waypoints.get(code)
        return string

    def print(self):
        print(self)
