import os
import json
import re, urllib
from configparser import ConfigParser
from pathlib import Path


class ConfigManager():
    """
    Class to handle service config. It loads json file from path, and
    config.ini file.
    """

    def __init__(self, json_path, json_path_dev):
        self.json_path = json_path
        self.json_path_dev = json_path_dev
        self.load_config_json_file()

    def load(self, os_var, variable, section=None):
        """
        Returns variable from config file.
        First see if there is the variable in the environment variables,
        if there is no variable, look in the config.ini file
        and if it does not exist either take from the json file
        """
        config_var = self.from_env_vars(os_var)
        if config_var:
            return config_var
        else:
            config =  self.from_config_json(
                self.config_json, variable, section)
            ini_file = self.check_if_path(config)
            if (ini_file):
                self.load_config_ini_file(ini_file)
                section, option = self.parse_path(config)
                config = self.from_config_ini(self.config_ini, section, option)
            return config
            
        return None

    def from_env_vars(self, var):
        """
        Returns variable from env vars
        """
        return os.environ.get(var, None)

    def from_config_ini(self, config, section, option):
        """
        Returns variable from config.ini file
        """
        try:
            value = config.get(section, option)            
            if value != 'true' and value != 'false':
                return value
            return value == 'true'
        except BaseException:
            return None

    def check_if_path(self, file):
        if (isinstance(file, str)):
            path = file.rsplit('/',2)
            file = Path(path[0])
            if file.is_file():
                return path[0]
            else:
                return None
        else:
            return None
    
    def parse_path(self, file):
        path = file.rsplit('/',2)
        section = path[1]
        option = path[2]
        return section, option

    def from_config_json(self, config, section, option):
        """
        Returns variable from json file
        """
        if (isinstance(config, dict)):
            field = config[section]
            if isinstance(field, dict):
                return field[option]
        return config[section]

    def load_config_ini_file(self, path):
        """
        Load confi.ini file from file path
        """
        try:
            config_ini = ConfigParser()
            configured_files = config_ini.read(path)
            if (configured_files):
                self.config_ini = config_ini
        except IOError:
            raise Exception('Error parsing config ini file')

    def load_config_json_file(self):
        """
        Load json file from file path
        """
        try:
            config_file = self.json_path
            if os.path.isfile(self.json_path_dev):
                config_file = self.json_path_dev
        except IOError:
            raise FileNotFoundError(
                'Configuration file not found: {}'.format(config_file))

        # Loads config from file
        with open(config_file) as json_data:
            try:
                self.config_json = json.load(json_data)
            except IOError:
                raise Exception('Error parsing JSON from config file')
