from pypilot.planner.coordinate import Coordinate
from pypilot.planner.geoutils import calc_tracking, calc_distance
from pypilot.planner.misc import clear
from pypilot.planner.waypoint import WayPoint
from pypilot.planner.waypointlist import WayPointList


class Planner:
    waypoints = []
    waypoint_list = WayPointList()

    def clear_waypoints(self):
        self.waypoints = []

    def read_waypoint(self, string):
        waypoint = self.waypoint_list.get_waypoint(string.upper())
        if waypoint:
            return waypoint

        print("Not a valid PSN code, attempting to parse as location")
        try:
            coord = Coordinate.from_string(string)
            return WayPoint(location=coord)
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
            print("%s,\t%.1f,\t,%.1f" % (next_waypoint.code, track, dist))
            current_waypoint = next_waypoint

    def load_waypoints(self):
        pass

    def save_waypoints(self):
        pass

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
                  "p) Print waypoint:\n"
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
                self.load_waypoints()
                clear()
            elif selection == 's':
                self.save_waypoints()
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
