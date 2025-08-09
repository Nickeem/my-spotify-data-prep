import os
import configparser

class Config:
    def __init__(self, config_file):
        self.CONFIG_FILE = config_file  # Path to the ini config file

    def get_config_value(self, section, key):
        config = configparser.ConfigParser()
        config.read(self.CONFIG_FILE)
        return config.get(section, key)

    def set_config_value(self, section, key, value):
        config = configparser.ConfigParser()
        config.read(self.CONFIG_FILE)