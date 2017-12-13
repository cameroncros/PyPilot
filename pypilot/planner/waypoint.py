class WayPoint:
    code = None
    state = None
    location = None
    coordinate = None

    def __init__(self, code=None, state=None, location=None, coordinate=None):
        self.code = code
        self.state = state
        self.location = location
        self.coordinate = coordinate

        if self.code is None and self.coordinate is None:
            raise ValueError("Either code or coordinate must be set.")

    def __str__(self):
        return "Code: %s,\tState: %s,  \tCoordinate: %s\tLocation: %s" % \
               (self.code, self.state, self.coordinate, self.location)

    def get_waypoint(self):
        if self.code:
            return self.code
        return str(self.coordinate)
