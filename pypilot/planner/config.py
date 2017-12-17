import json
import os
import pkg_resources
from shutil import copyfile
from pathlib import Path

# noinspection PyTypeChecker
RESOURCES = "resources"


class Config:
    _instance = None
    config = None
    config_dir = None

    # noinspection PyArgumentList
    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        homedir = str(Path.home())
        self.config_dir = homedir + os.sep + ".pypilot"

        if not os.path.isdir(self.config_dir):
            os.mkdir(self.config_dir)

        filelist = pkg_resources.resource_listdir(__name__, RESOURCES)
        for file in filelist:
            file = self.config_dir + os.sep + file
            if not os.path.isfile(file):
                resource_path = "/".join((RESOURCES, file))
                template = pkg_resources.resource_filename(__name__, resource_path)
                copyfile(template, file)

    def load_config(self):
        config_file = self.config_dir + os.sep + "config.json"
        with open(config_file, "r") as file:
            json_string = file.read()
            self.config = json.loads(json_string)
        # Validate config is correct
        if (not self.config.get("magnetic_north")):
            print("Open the config file: %s, and add a magnetic_north "
                  "element like: \"magnetic_north\": [80.4, 72.8], "
                  "Update with the closest magnetic north coordinate you can get" % config_file)
            exit(0)

    def get_magnetic_north(self):
        if self.config is None:
            self.load_config()
        magnetic_north = self.config['magnetic_north']
        return magnetic_north[0], magnetic_north[1]

    def get_waypoint_lists(self):
        if self.config is None:
            self.load_config()
        filenames = self.config.get('waypoint_files')
        return [(self.config_dir + os.sep + name) for name in filenames]