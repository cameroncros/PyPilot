import csv

from pypilot.planner.coordinate import Coordinate
from pypilot.planner.utils import calc_tracking, calc_distance
from pypilot.planner.misc import clear
from pypilot.planner.waypoint import WayPoint
from pypilot.planner.waypointlist import WayPointList


class Planner:
    waypoints = None
    waypoint_list = None

    def __init__(self):
        self.waypoints = []
        self.waypoint_list = WayPointList()
        try:
            self.load_waypoint_list("positions.csv")
        except FileNotFoundError:
            print("Failed to load positions.csv")

    def load_waypoint_list(self, filename):
        self.waypoint_list.load_waypoints(filename)

    def clear_waypoints(self):
        self.waypoints = []

    def read_waypoint(self, string):
        waypoint = self.waypoint_list.get_waypoint(string.upper())
        if waypoint:
            return waypoint

        print("Not a valid PSN code, attempting to parse as location")
        try:
            coord = Coordinate.from_string(string)
            return WayPoint(coordinate=coord)
        except ValueError:
            print("Failed to parse as GPS lat long coordinate.")

        return None

    def input_waypoints(self):
        print("Input waypoints as PSN codes, or as (lat, lon), end with a blank line to exit:\n")
        i = len(self.waypoints) + 1
        while True:
            last = input("%s)" % i)
            if last == "":
                break
            waypoint = self.read_waypoint(last)
            if waypoint:
                self.waypoints.append(waypoint)
                i += 1

    def delete_waypoint(self):
        self.print_waypoints()
        i = input("Which waypoint would you like removed?: ")
        self.waypoints.remove(i - 1)

    def insert_waypoint(self):
        self.print_waypoints()

        index = int(input("Insert waypoints after:"))

        print("Input waypoints as PSN codes, or as (lat, lon), end with a blank line to exit:\n")
        while True:
            last = input("%s)" % index)
            if last == "":
                break
            waypoint = self.read_waypoint(last)
            if waypoint:
                self.waypoints.insert(index, waypoint)
                index += 1

    def print_waypoints(self):
        i = 1
        for waypoint in self.waypoints:
            print("%s) %s" % (i, waypoint))
            i += 1

    def print_flight_plan(self):
        print("PSN,\tTRK (True),\tDIST")
        current_waypoint = self.waypoints[0]
        print("%s" % current_waypoint.code)
        for i in range(1, len(self.waypoints)):
            next_waypoint = self.waypoints[i]
            track = calc_tracking(current_waypoint, next_waypoint)
            dist = calc_distance(current_waypoint, next_waypoint)
            print("%s,\t%.1f,\t,%.1f" % (next_waypoint.get_waypoint(), track, dist))
            current_waypoint = next_waypoint

    def load_waypoints(self, filename):
        self.clear_waypoints()
        with open(filename, 'r') as file:
            csvreader = csv.reader(file, delimiter=',')
            for row in csvreader:
                if row[0].startswith("PSN") or row[0] == "":
                    continue
                waypoint = self.read_waypoint(row[0])
                if waypoint is None:
                    raise Exception("Failed to parse save file line: %s", ", ".join(row))
                self.waypoints.append(waypoint)

    def save_waypoints(self, filename):
        with open(filename, 'w') as file:
            csvwriter = csv.writer(file, delimiter=',')

            csvwriter.writerow(["PSN", "TRK (True)", "DIST"])
            prev_waypoint = self.waypoints[0]
            csvwriter.writerow([prev_waypoint.get_waypoint()])
            for i in range(1, len(self.waypoints)):
                next_waypoint = self.waypoints[i]
                track = calc_tracking(prev_waypoint, next_waypoint)
                dist = calc_distance(prev_waypoint, next_waypoint)
                csvwriter.writerow([next_waypoint.get_waypoint(), track, dist])
                prev_waypoint = next_waypoint

    def main(self):
        print("Welcome to the pilot trip planning tool. \n"
              "Please use caution with this tool, as it may not be correct, "
              "check manually with your charts to be sure.")

        while True:
            print("Choose:\n"
                  "c) Clear route\n"
                  "l) Load route (CSV)\n"
                  "s) Save route (CSV)\n"
                  "a) Add waypoints\n"
                  "d) Delete waypoint\n"
                  "i) Insert waypoint\n"
                  "p) Print waypoints:\n"
                  "pa) Print all known waypoints:\n"
                  "fp) Print flightplan:\n"
                  "0) Exit")
            selection = input("Option: ")

            if selection == 'c':
                self.clear_waypoints()
                clear()
            elif selection == 'a':
                self.input_waypoints()
                clear()
            elif selection == 'l':
                filename = input("Filename to read from: ")
                self.load_waypoints(filename)
                clear()
            elif selection == 's':
                filename = input("Filename to save to: ")
                self.save_waypoints(filename)
                clear()
            elif selection == 'd':
                self.delete_waypoint()
                clear()
            elif selection == 'i':
                self.insert_waypoint()
                clear()
            elif selection == 'p':
                clear()
                self.print_waypoints()
            elif selection == 'pa':
                clear()
                self.waypoint_list.print()
            elif selection == 'fp':
                clear()
                self.print_flight_plan()
            elif selection == '0':
                break


if __name__ == "__main__":
    Planner().main()
