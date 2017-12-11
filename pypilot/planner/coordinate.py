import re

from pypilot.planner.latlong import LatLong


class Coordinate:
    latitude = None
    longitude = None

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    @classmethod
    def from_string(cls, string):
        parts = re.sub("[0-9.,]", "", string).split(",")
        if len(parts) != 2:
            raise ValueError
        return cls(LatLong(parts[0]), LatLong(parts[1]))

    def to_tuple(self):
        return self.latitude.degrees, self.longitude.degrees

    def __str__(self):
        return "(%s, %s)" % (self.latitude, self.longitude)
