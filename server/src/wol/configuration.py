__author__ = 'archeg'
import json


class ConfigService():
    def __init__(self):
        self.json_data = json.load(open('config.json', 'r'))

    def get_config(self, key):
        """ Returns configuration from a config file by given key
        """
        return self.json_data["config"][key]
