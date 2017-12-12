class LatLong:
    degrees = None

    def __init__(self, degrees):
        self.degrees = float(degrees)

    @classmethod
    def from_parts(cls, direction, degrees, minutes=None):
        val = float(degrees)
        if minutes:
            val += (float(minutes) / 60)
        if direction in {'S', 'W'}:
            val *= -1
        return cls(val)

    def __str__(self):
        return "%.4f" % self.degrees

    def __float__(self):
        return self.degrees
