import os
import logging.config
import ast
import json
from configparser import ConfigParser
from utils.config_parser import field_config_file
from utils.json_parser import from_json

APP_NAME = "notifyme"
APP_CHARSET = 'UTF-8'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Config file paths
CONFIGURATION_FILE = 'config.json'
CONFIGURATION_FILE_DEV = 'config_development.json'

try:
    config_file = CONFIGURATION_FILE
    if os.path.isfile(CONFIGURATION_FILE_DEV):
        config_file = CONFIGURATION_FILE_DEV
except IOError:
    raise FileNotFoundError('Configuration file not found: {}'.format(config_file))

# Loads config from file
with open(config_file) as json_data:
    try:    
        config = json.load(json_data)
    except IOError:
        raise Exception('Error parsing JSON from config file')

CONFIGURATION_FILE = config['config_ini_file']

if CONFIGURATION_FILE:
    # Carga de la configuration externa
    try:
        config_ini = ConfigParser()
        configured_files = config_ini.read(CONFIGURATION_FILE)
        if (configured_files):
            config = config_ini
    except:
        pass

LOG_ROOT_PATH = field_config_file(config, 'loggin', 'root_path')
RABBITMQ_SERVER = field_config_file(config, 'bus', 'host')
RABBITMQ_USER = field_config_file(config, 'bus', 'user')
RABBITMQ_PASSWORD = field_config_file(config, 'bus', 'password')
RABBITMQ_QUEUE = field_config_file(config, 'bus', 'queue_name')
RABBIRMQ_EXCHANGE_ERROR = field_config_file(config, 'bus', 'error_exchange')

SMTP_EMAIL = field_config_file(config, 'smtp', 'email')
SMTP_HOST = field_config_file(config, 'smtp', 'server')
SMTP_PORT = field_config_file(config, 'smtp', 'port')
SMTP_PASS = field_config_file(config, 'smtp', 'password')

DB_SERVER = os.getenv('DB_SERVER', '172.17.0.3')
DB_PORT = os.getenv('DB_HOST', 28015)

DB_NAME = 'notify_me'

REFRESH_DATABASE = field_config_file(config, 'db', 'refresh_database')

DEFAULT_TEMPLATE_TEXT = field_config_file(config, 'default_template', 'text')
DEFAULT_TEMPLATE_SUBJECT = field_config_file(config, 'default_template', 'text')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "%(asctime)s.%(msecs)04d %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)-7s:  %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'notify_me': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# Logger inicialization
logging.config.dictConfig(LOGGING)
logger = logging.getLogger('notify_me')

