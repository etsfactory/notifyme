import os
import json
from configparser import ConfigParser

class ConfigManager():
    """
    Class to handle service config. It loads json file from path, and
    config.ini file.
    """
    def __init__(self, json_path, json_path_dev, config_ini_path):
        self.json_path = json_path
        self.json_path_dev = json_path_dev
        self.config_ini_path = config_ini_path
        self.load_config_ini_file(self.config_ini_path)
        self.load_config_json_file(self.json_path, self.json_path_dev)

    def load(self, os_var, variable, section=None):
        """
        Returns variable from config file. 
        First see if there is a variable in the system environment variables, 
        if there is no variable, look in the config.ini file 
        and if it does not exist either take from the json file
        """
        config_var = self.from_env_vars(os_var)
        if config_var:
            return config_var
        else:
            if hasattr(self, 'config_ini'):
                try:
                    config = self.from_config_ini(self.config_ini, variable, section)
                    if config != None:
                        return config
                    else: 
                        return self.from_config_json(self.config_json, variable, section)
                except IOError:
                    raise Exception('Error parsing config file ini')
            else:
                return self.from_config_json(self.config_json, variable, section)
        
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
        except:
            return None

    def from_config_json(self, config, section, option):
        """
        Returns variable from json file
        """
        if (isinstance(config, dict)):
            field = config[section]
            if isinstance(field, dict):
                return field[option]
        return config[section]

    def load_config_ini_file(self, file):
        """
        Load confi.ini file from file path
        """
        try:
            config_ini = ConfigParser()
            configured_files = config_ini.read(file)
            if (configured_files):
                self.config_ini = config_ini
        except IOError:
            raise Exception('Error parsing config file ini')

    def load_config_json_file(self, file, file_dev):
        """
        Load json file from file path
        """
        try:
            config_file = file
            if os.path.isfile(file_dev):
                config_file = file_dev
        except IOError:
            raise FileNotFoundError('Configuration file not found: {}'.format(config_file))

        # Loads config from file
        with open(config_file) as json_data:
            try:  
                self.config_json = json.load(json_data)
            except IOError:
                raise Exception('Error parsing JSON from config file')

   