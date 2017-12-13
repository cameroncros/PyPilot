import json


# noinspection PyTypeChecker
class Config:
    _instance = None

    # noinspection PyArgumentList
    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    config = None

    def load_config(self):
        with open("config.json", "r") as file:
            json_string = file.read()
            self.config = json.loads(json_string)

    def get_magnetic_north(self):
        if self.config is None:
            self.load_config()
        magnetic_north = self.config['magnetic_north']
        return magnetic_north[0], magnetic_north[1]

    def get_waypoint_lists(self):
        if self.config is None:
            self.load_config()
        return self.config.get('waypoint_files')
