import csv

from pypilot.planner.config import Config
from pypilot.planner.coordinate import Coordinate
from pypilot.planner.geoutils import calc_distance, calc_tracking_magnetic, calc_tracking
from pypilot.planner.waypoint import WayPoint
from pypilot.planner.waypointlist import WayPointList


class Planner:
    waypoints = None
    waypoint_list = None

    def __init__(self):
        self.waypoints = []
        self.waypoint_list = WayPointList()
        for waypoint_file in Config().get_waypoint_lists():
            try:
                self.load_waypoint_list(waypoint_file)
            except FileNotFoundError:
                print("Failed to load: %s" % waypoint_file)

    def load_waypoint_list(self, filename):
        self.waypoint_list.load_waypoints(filename)

    def clear_waypoints(self):
        self.waypoints = []

    def read_waypoint(self, string):
        waypoint = self.waypoint_list.get_waypoint(string.upper())
        if waypoint:
            return waypoint
        try:
            coord = Coordinate.from_string(string)
            return WayPoint(coordinate=coord)
        except ValueError:
            pass

        print("Failed to parse as GPS or PSN coordinate.")
        return None

    def delete_waypoint(self):
        self.print_waypoints()
        i = input("Which waypoint would you like removed?: ")
        self.waypoints.remove(int(i) - 1)

    def insert_waypoint(self, string, index=-1):
        if string == "":
            return
        waypoint = self.read_waypoint(string)
        if waypoint:
            self.waypoints.insert(index, waypoint)
            index += 1

    def print_waypoints(self):
        i = 1
        for waypoint in self.waypoints:
            print("%s) %s" % (i, waypoint))
            i += 1

    def print_flight_plan(self):
        if len(self.waypoints) < 2:
            print("Need at least 2 way points for a flightplan!")
            return
        print("PSN,\tTRK (T),\tTRK (M),\tDIST")
        current_waypoint = self.waypoints[0]
        print("%s" % current_waypoint.code)
        for i in range(1, len(self.waypoints)):
            next_waypoint = self.waypoints[i]
            track_t = calc_tracking(current_waypoint, next_waypoint)
            track_m = calc_tracking_magnetic(current_waypoint, next_waypoint)
            dist = calc_distance(current_waypoint, next_waypoint)
            print("%s,\t%.1f,\t%.1f,\t%.1f" % (next_waypoint.get_waypoint(), track_t, track_m, dist))
            current_waypoint = next_waypoint

    def load_waypoints(self, filename):
        self.clear_waypoints()
        with open(filename, 'r') as file:
            csvreader = csv.reader(file, delimiter=',', lineterminator='\n')
            for row in csvreader:
                if len(row) == 0 or row[0].startswith("PSN") or row[0] == "":
                    continue
                waypoint = self.read_waypoint(row[0])
                if waypoint is None:
                    raise Exception("Failed to parse save file line: %s", ", ".join(row))
                self.waypoints.append(waypoint)

    def save_waypoints(self, filename):
        with open(filename, 'w') as file:
            csvwriter = csv.writer(file, delimiter=',', lineterminator='\n')

            csvwriter.writerow(["PSN", "TRK (T)", "TRK (M-est)", "DIST"])
            prev_waypoint = self.waypoints[0]
            csvwriter.writerow([prev_waypoint.get_waypoint()])
            for i in range(1, len(self.waypoints)):
                next_waypoint = self.waypoints[i]
                track_t = calc_tracking_magnetic(prev_waypoint, next_waypoint)
                track_m = calc_tracking_magnetic(prev_waypoint, next_waypoint)
                dist = calc_distance(prev_waypoint, next_waypoint)
                csvwriter.writerow([next_waypoint.get_waypoint(), track_t, track_m, dist])
                prev_waypoint = next_waypoint
