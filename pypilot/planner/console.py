import glob
import cmd
import sys
import os

from pypilot.planner.planner import Planner


def _append_slash_if_dir(p):
    if p and os.path.isdir(p) and p[-1] != os.sep:
        return p + os.sep
    else:
        return p


# noinspection PyUnusedLocal
def _autocomplete_file_path(text, line, begidx, endidx):
    """ File path autocompletion, used with the cmd module complete_* series functions"""
    # http://stackoverflow.com/questions/16826172/filename-tab-completion-in-cmd-cmd-of-python
    before_arg = line.rfind(" ", 0, begidx)
    if before_arg == -1:
        return  # arg not found

    fixed = line[before_arg + 1:begidx]  # fixed portion of the arg
    arg = line[before_arg + 1:endidx]
    pattern = arg + '*'

    completions = []
    for path in glob.glob(pattern):
        path = _append_slash_if_dir(path)
        completions.append(path.replace(fixed, "", 1))
    return completions


class Console(cmd.Cmd):
    planner = Planner()

    prompt = "PyPilot> "
    intro = "Welcome to the pilot trip planning tool. \n" \
            "Please use caution with this tool, as it may not be correct, " \
            "check manually with your charts to be sure."

    def do_help(self, line):
        print("Choose:\n"
              "load [filename]) Load route (CSV)\n"
              "save [filename]) Save route (CSV)\n"
              "clear) Clear route\n"
              "delete) Delete waypoint\n"
              "insert) Insert waypoint\n"
              "print) Print waypoints:\n"
              "list) Print all known waypoints:\n"
              "printplan) Print flightplan:\n"
              "exit) Exit")

    # noinspection PyUnusedLocal
    def do_clear(self, line):
        self.planner.clear_waypoints()

    def do_search(self, line):
        i = 0
        line = line.upper()
        for key in self.planner.waypoint_list.waypoints:
            waypoint = self.planner.waypoint_list.get_waypoint(key)
            stat_list = [waypoint.code, waypoint.state, str(waypoint.coordinate), waypoint.location]
            if any(line in s for s in stat_list):
                print("%i) %s" % (i, str(waypoint)))
                i += 1

    def do_insert(self, line):
        if line:
            self.planner.insert_waypoint(line)

    # noinspection PyUnusedLocal
    def complete_insert(self, text, line, start_index, end_index):
        commands = list(self.planner.waypoint_list.waypoints.keys())
        commands.sort()
        if text:
            return [
                command for command in commands
                if command.startswith(text.strip())
            ]
        else:
            return commands

    # noinspection PyUnusedLocal
    def do_print(self, line):
        self.planner.print_waypoints()

    # noinspection PyUnusedLocal
    def do_plan(self, line):
        self.planner.print_flight_plan()

    def do_load(self, path):
        self.planner.load_waypoints(path)

    @staticmethod
    def complete_load(text, line, start_index, end_index):
        return _autocomplete_file_path(text, line, start_index, end_index)

    def do_save(self, path):
        self.planner.save_waypoints(path)

    @staticmethod
    def complete_save(text, line, start_index, end_index):
        return _autocomplete_file_path(text, line, start_index, end_index)

    def default(self, line):
        self.planner.insert_waypoint(line)

    # noinspection PyUnusedLocal
    @staticmethod
    def do_exit(line):
        print('\n')
        return True

    def cmdloop_with_keyboard_interrupt(self):
        do_quit = False
        while not do_quit:
            try:
                self.cmdloop()
                do_quit = True
            except KeyboardInterrupt:
                sys.stdout.write('\n')
                exit(0)


if __name__ == "__main__":
    Console().cmdloop()
