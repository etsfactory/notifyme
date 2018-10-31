import os
import logging.config
import json
from configparser import ConfigParser


APP_NAME = "notify.me"

# Config file paths
CONFIGURATION_FILE = 'config.json'
CONFIGURATION_FILE_DEV = 'config_development.json'

try:
    config_file = CONFIGURATION_FILE
    if os.path.isfile(CONFIGURATION_FILE_DEV):
        config_file = CONFIGURATION_FILE_DEV
except IOError:
    print('Error finding config file')

# Loads confid from file
with open(config_file) as json_data:
    try:    
        print(config_file)
        config = json.load(json_data)
    except IOError:
        print('JSON loading problem')


LOG_ROOT_PATH = config['loggin']
RABBITMQ = config['rabbitmq']
RABBITMQ_SERVER = RABBITMQ['server']
RABBITMQ_USER = RABBITMQ['user']
RABBITMQ_PASSWORD = RABBITMQ['password']

SMTP = config['smtp']
SMTP_EMAIL = SMTP['email']
SMTP_HOST = SMTP['server']
SMTP_PORT = SMTP['port']
SMTP_PASS = SMTP['password']

DB_SERVER = os.getenv('DB_SERVER', '172.17.0.2')
DB_PORT = os.getenv('DB_HOST', 28015)

DB_NAME = 'notify_me'

USERS = config['users']

DEFAULT_TEMPLATE = config['default_template']
DEFAULT_TEMPLATE_NAME = DEFAULT_TEMPLATE['name']
DEFAULT_TEMPLATE_TEXT = DEFAULT_TEMPLATE['text']
DEFAULT_TEMPLATE_SUBJECT = DEFAULT_TEMPLATE['subject']

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