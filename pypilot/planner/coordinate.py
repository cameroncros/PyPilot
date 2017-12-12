import re

from pypilot.planner.latlong import LatLong


class Coordinate:
    coords = None

    def __init__(self, latitude, longitude):
        self.coords = (latitude, longitude)

    @classmethod
    def from_string(cls, string):
        parts = re.sub("[^0-9.,]", "", string).split(",")
        if len(parts) != 2:
            raise ValueError
        return cls(LatLong(parts[0]), LatLong(parts[1]))

    def __str__(self):
        return "(%s, %s)" % (self.coords[0], self.coords[1])

    def __iter__(self):
        for i in range(len(self.coords)):
            yield float(self.coords[i])
